import json
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    ConnectionClosedError,
    EndpointConnectionError,
)
from loguru import logger

from app.config import settings
from app.distributor.base import BaseDistributor


class SESDistributor(BaseDistributor):
    """使用 AWS SES 发送邮件的分发器"""

    def __init__(self):
        # 调用父类初始化
        super().__init__(settings.SES_EMAIL_SENDER)

        self.aws_region = settings.AWS_REGION
        self.aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY

        # 创建带有重试配置的 SES 客户端
        config = Config(
            region_name=self.aws_region,
            retries={"max_attempts": 5, "mode": "adaptive"},
            connect_timeout=10,
            read_timeout=180,
            max_pool_connections=10,
            tcp_keepalive=True,
        )

        try:
            self.ses_client = boto3.client(
                "ses",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                config=config,
            )
            # 验证 SES 客户端
            self._verify_ses_client()

        except Exception as e:
            logger.error(f"初始化 SES 客户端失败: {str(e)}")
            raise RuntimeError("AWS SES 初始化失败，请检查配置") from e

    def _verify_ses_client(self):
        """验证 SES 客户端配置"""
        try:
            # 测试 AWS 凭证
            sts = boto3.client(
                "sts",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region,
            )
            identity = sts.get_caller_identity()
            logger.info(f"AWS 凭证验证成功，账户 ID: {identity['Account']}")

            # 检查 SES 服务状态
            response = self.ses_client.get_send_quota()
            logger.info(f"SES 发送配额: {json.dumps(response, indent=2)}")

            # 检查发件人是否已验证
            response = self.ses_client.get_identity_verification_attributes(
                Identities=[self.sender_email]
            )
            status = (
                response["VerificationAttributes"]
                .get(self.sender_email, {})
                .get("VerificationStatus")
            )

            if not status or status != "Success":
                logger.warning(
                    f"发件人邮箱 {self.sender_email} 未验证，"
                    f"当前状态: {status or '未找到'}"
                )
                logger.info("请在 AWS SES 控制台验证发件人邮箱")

        except EndpointConnectionError as e:
            logger.error(f"无法连接到 AWS SES 服务: {str(e)}")
            logger.info(f"请检查网络连接和区域设置 (当前区域: {self.aws_region})")
            raise
        except (ClientError, BotoCoreError) as e:
            logger.error(f"验证 SES 客户端失败: {str(e)}")
            if "InvalidClientTokenId" in str(e):
                logger.info("AWS Access Key ID 无效")
            elif "SignatureDoesNotMatch" in str(e):
                logger.info("AWS Secret Access Key 无效")
            elif "UnrecognizedClientException" in str(e):
                logger.info("AWS 凭证无效")
            raise RuntimeError("AWS SES 配置无效，请检查凭证和权限设置") from e

    def _send_email(self, msg: MIMEMultipart, email: str) -> bool:
        """发送邮件"""
        try:
            logger.debug(f"正在发送邮件到 {email}")
            logger.debug(f"发件人: {self.sender_email}")

            # 获取邮件大小
            email_size = len(msg.as_string())
            logger.debug(f"邮件大小: {email_size / 1024 / 1024:.2f}MB")

            # 检查邮件大小
            if email_size > 10 * 1024 * 1024:  # 10MB
                logger.warning("邮件大小超过10MB，将使用云存储预签名URL")
                return False

            # 尝试发送邮件
            for attempt in range(3):
                try:
                    response = self.ses_client.send_raw_email(
                        Source=self.sender_email,
                        Destinations=[email],
                        RawMessage={"Data": msg.as_string()},
                    )
                    logger.debug(
                        f"邮件发送成功，MessageId: {response.get('MessageId')}"
                    )
                    return True
                except ConnectionClosedError as e:
                    if attempt < 2:
                        logger.warning(
                            f"连接被关闭，正在重试 ({attempt + 1}/3), 错误信息: {e}"
                        )
                        continue
                    raise ConnectionError("连接被关闭，无法发送邮件") from e
            else:
                logger.error("重试3次后仍然无法发送邮件")
                return False

        except EndpointConnectionError as e:
            logger.error(f"发送邮件时连接失败: {str(e)}")
            logger.info("请检查网络连接和防火墙设置")
            raise ConnectionError("无法连接到AWS SES服务，请检查网络连接") from e
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            logger.error(f"AWS SES 错误: {error_code} - {error_message}")

            if error_code == "MessageRejected":
                if "Email address is not verified" in error_message:
                    logger.info(
                        f"请确保邮箱 {email} 已在 AWS SES 中验证（沙箱模式下需要验证所有收件人）"
                    )
                elif "Maximum message size exceeded" in error_message:
                    logger.info("邮件大小超过限制（最大 10MB），将使用云存储预签名URL")
                    return False
            elif error_code == "InvalidParameterValue":
                logger.info("邮件格式无效，请检查邮件内容")
            raise RuntimeError("AWS SES 配置无效，请检查凭证和权限设置") from e
        except Exception as e:
            logger.error(f"发送邮件时发生未知错误: {str(e)}")
            raise RuntimeError("发送邮件时发生未知错误") from e

    async def send_book(
        self,
        book_dict: dict,
        email: str,
        subject: Optional[str] = None,
        message: Optional[str] = None,
    ) -> bool:
        """发送单本书籍"""
        try:
            msg = await self.create_book_email(book_dict, email, subject, message)
            return self._send_email(msg, email)
        except Exception as e:
            logger.error(f"发送书籍失败: {str(e)}")
            raise

    async def send_books(
        self,
        book_dicts: List[dict],
        email: str,
        subject: Optional[str] = None,
        message: Optional[str] = None,
    ) -> bool:
        """批量发送多本书籍"""
        try:
            msg = await self.create_books_email(book_dicts, email, subject, message)
            return self._send_email(msg, email)
        except Exception as e:
            logger.error(f"发送书籍失败: {str(e)}")
            raise
