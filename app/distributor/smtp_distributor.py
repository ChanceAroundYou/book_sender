import smtplib
from email.mime.multipart import MIMEMultipart
from typing import List

from loguru import logger

from app.config import settings
from app.distributor.base import BaseDistributor


class SMTPDistributor(BaseDistributor):
    """邮件分发器，用于将书籍通过SMTP邮件发送"""

    def __init__(self):
        # 调用父类初始化
        super().__init__(settings.SMTP_SENDER_EMAIL)
        
        # SMTP设置
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD

    def _send_email(self, msg: MIMEMultipart, email: str) -> bool:
        """发送邮件"""
        logger.debug(f"正在发送邮件到 {email}")
        logger.debug(f"发件人: {self.sender_email}")
        
        # 获取邮件大小
        email_size = len(msg.as_string())
        logger.debug(f"邮件大小: {email_size / 1024 / 1024:.2f}MB")

        # 最大重试次数
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                logger.debug(f"尝试发送邮件 (第{retry_count + 1}次)")
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    logger.debug("已建立SMTP SSL连接")
                    server.login(self.smtp_username, self.smtp_password)
                    logger.debug("SMTP登录成功")
                    server.send_message(msg)
                    logger.info(f"邮件发送成功: {email}")
                return True

            except smtplib.SMTPAuthenticationError as e:
                logger.error(f"SMTP认证失败: {str(e)}")
                raise RuntimeError("SMTP认证失败，请检查用户名和密码") from e

            except (smtplib.SMTPServerDisconnected, ConnectionError) as e:
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"连接断开，正在重试 ({retry_count}/{max_retries}): {str(e)}")
                    continue
                logger.error(f"重试{max_retries}次后仍然失败")
                raise ConnectionError("无法连接到SMTP服务器，请检查网络连接") from e

            except smtplib.SMTPException as e:
                logger.error(f"SMTP错误: {str(e)}")
                raise RuntimeError(f"SMTP错误: {str(e)}") from e

            except Exception as e:
                logger.error(f"发送邮件时发生未知错误: {str(e)}")
                raise RuntimeError("发送邮件时发生未知错误") from e
        return False

    async def send_book(self, 
                       book_dict: dict, 
                       email: str,
                       subject: str | None = None,
                       message: str | None = None) -> bool:
        """发送单本书籍"""
        try:
            msg = await self.create_book_email(book_dict, email, subject, message)
            return self._send_email(msg, email)
        except Exception as e:
            logger.error(f"发送书籍失败: {str(e)}")
            raise
            
    async def send_books(self, 
                        book_dicts: List[dict], 
                        email: str,
                        subject: str | None = None,
                        message: str | None = None) -> bool:
        """批量发送多本书籍"""
        try:
            msg = await self.create_books_email(book_dicts, email, subject, message)
            return self._send_email(msg, email)
        except Exception as e:
            logger.error(f"发送书籍失败: {str(e)}")
            raise
