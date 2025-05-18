import smtplib
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

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
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)

    async def send_book(self, 
                       book_dict: dict, 
                       email: str,
                       subject: Optional[str] = None,
                       message: Optional[str] = None) -> bool:
        """
        发送单本书籍到指定邮箱
        
        Args:
            book_dict: 书籍字典
            email: 收件人邮箱
            subject: 邮件主题
            message: 邮件正文
            
        Returns:
            bool: 发送是否成功
        """
        try:
            # 创建邮件对象
            msg = self.create_book_email(book_dict, email, subject, message)
            self._send_email(msg, email)
            logger.info(f"成功发送邮件：{email}")
            return True
        except Exception as e:
            logger.error(f"发送邮件失败: {str(e)}")
            raise e
            
    async def send_books(self, 
                        book_dicts: List[dict], 
                        email: str,
                        subject: Optional[str] = None,
                        message: Optional[str] = None) -> bool:
        """
        批量发送多本书籍到指定邮箱
        
        Args:
            book_dicts: 书籍字典列表
            email: 收件人邮箱
            subject: 邮件主题
            message: 邮件正文
            
        Returns:
            bool: 发送是否成功
        """
        try:
            msg = self.create_books_email(book_dicts, email, subject, message)
            self._send_email(msg, email)
            logger.info(f"成功发送邮件：{email}")
            return True
        except Exception as e:
            logger.error(f"发送邮件失败: {str(e)}")
            raise e
