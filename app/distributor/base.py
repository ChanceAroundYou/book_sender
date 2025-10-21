import os
from abc import ABC, abstractmethod
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Tuple

from loguru import logger

from app.config import settings
from app.uploader import create_uploader




class BaseDistributor(ABC):
    """分发器基类，定义分发器接口"""

    def __init__(self, sender_email: str):
        self.sender_email = sender_email
        self.uploader = create_uploader(settings.UPLOADER_TYPE)

    @staticmethod
    def get_mime_subtype(file_format: str) -> str:
        """根据文件格式获取对应的 MIME subtype
            
        Args:
            file_format: 文件格式 (pdf, epub, mobi 等)
            
        Returns:
            str: MIME subtype
        """
        # 标准化文件格式
        format_lower = file_format.lower().strip('.')
        
        # 常见电子书和文档格式
        DOCUMENT_TYPES = {
            'pdf': 'pdf',
            'epub': 'epub+zip',
            'mobi': 'x-mobipocket-ebook',
            'azw3': 'vnd.amazon.ebook',
            'doc': 'msword',
            'docx': 'vnd.openxmlformats-officedocument.wordprocessingml.document',
            'rtf': 'rtf',
        }
        
        # 压缩文件格式
        ARCHIVE_TYPES = {
            'zip': 'zip',
            'rar': 'x-rar-compressed',
            '7z': 'x-7z-compressed',
            'gz': 'gzip',
        }
        # 查找对应的 MIME subtype
        if format_lower in DOCUMENT_TYPES:
            return DOCUMENT_TYPES[format_lower]
        elif format_lower in ARCHIVE_TYPES:
            return ARCHIVE_TYPES[format_lower]
        # 默认返回 octet-stream
        return 'octet-stream' 

    @abstractmethod
    async def send_book(self, 
                       book_dict: dict, 
                       email: str,
                       subject: str | None = None,
                       message: str | None = None) -> bool:
        """
        分发单本书籍
        
        Args:
            book_dict: 书籍字典
            email: 收件人邮箱
            subject: 邮件主题
            message: 邮件正文
        Returns:
            bool: 分发是否成功
        """
        pass

    @abstractmethod
    async def send_books(self, 
                        book_dicts: List[dict], 
                        email: str,
                        subject: str | None = None,
                        message: str | None = None) -> bool:
        """
        批量分发多本书籍
        
        Args:
            book_dicts: 书籍字典列表
            email: 收件人邮箱
            subject: 邮件主题
            message: 邮件正文
        Returns:
            bool: 分发是否成功
        """
        pass

    async def _get_url(self, file_path: str, expires_in: int = 604800) -> Tuple[str, str]:
        """上传文件并获取URL
        
        Args:
            file_path: 文件路径
            expires_in: URL有效期（秒）
            
        Returns:
            Tuple[str, str]: (文件键名, 访问URL)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        # 获取上传器
        # 生成文件键名
        key = os.path.basename(file_path)
        # 上传文件并获取URL
        url = self.uploader.get_url(file_path, key, expires_in)
        
        return key, url

    def _should_use_uploader(self, file_size: int, max_attachment_size: int = 10 * 1024 * 1024) -> bool:
        """判断是否应该使用上传器
        
        Args:
            file_size: 文件大小（字节）
            max_attachment_size: 最大附件大小（字节），默认10MB
            
        Returns:
            bool: 是否应该使用上传器
        """
        return file_size > max_attachment_size

    async def create_book_email(self, 
                         book_dict: dict,
                         email: str,
                         subject: str | None = None,
                         message: str | None = None) -> MIMEMultipart:
        """
        创建单本书籍的邮件对象
        
        Args:
            book_dict: 书籍字典
            email: 收件人邮箱
            subject: 邮件主题
            message: 邮件正文
            
        Returns:
            MIMEMultipart: 邮件对象
        """
        if not email:
            raise ValueError("收件人邮箱不能为空")
        
        book_title = book_dict.get('title', '')
        file_path = book_dict.get('file_path', '')
        file_format = book_dict.get('file_format', '')
        file_size = book_dict.get('file_size', 0)

        msg = MIMEMultipart()
        msg['Subject'] = subject or f"发送书籍：《{book_title}》"
        msg['From'] = f"Book Sender <{self.sender_email}>"
        msg['To'] = email

        # 如果文件太大，使用上传器
        if self._should_use_uploader(file_size):
            try:
                key, url = await self._get_url(file_path)
                body = message or self._generate_book_email_body_with_url(book_dict, url)
            except Exception as e:
                logger.error(f"文件上传失败: {str(e)}")
                raise e
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
        elif file_path and os.path.exists(file_path):
            body = message or self._generate_book_email_body(book_dict)
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            with open(file_path, 'rb') as f:
                mime_subtype = self.get_mime_subtype(file_format)
                book_file = MIMEApplication(f.read(), _subtype=mime_subtype)
                filename = os.path.basename(file_path)
                book_file.add_header('Content-Disposition', 'attachment', 
                                   filename=('utf-8', '', filename))
                msg.attach(book_file)
        else:
            logger.warning(f"文件未找到: {file_path}")
            raise FileNotFoundError(f"文件未找到: {file_path}")

        return msg

    async def create_books_email(self,
                          book_dicts: List[dict],
                          email: str,
                          subject: str | None = None,
                          message: str | None = None) -> MIMEMultipart:
        """
        创建多本书籍的邮件对象
        
        Args:
            book_dicts: 书籍字典列表
            email: 收件人邮箱
            subject: 邮件主题
            message: 邮件正文
            
        Returns:
            MIMEMultipart: 邮件对象
        """
        if not email:
            raise ValueError("收件人邮箱不能为空")

        book_titles = [book_dict.get('title', '') for book_dict in book_dicts]
        
        msg = MIMEMultipart()
        msg['Subject'] = subject or f"发送书籍{len(book_dicts)}本: {', '.join(['《'+title+'》' for title in book_titles])}"
        msg['From'] = f"Book Sender <{self.sender_email}>"
        msg['To'] = email

        # 处理每本书
        book_links = []
        for book_dict in book_dicts:
            file_path = book_dict.get('file_path', '')
            
            if not file_path or not os.path.exists(file_path):
                logger.warning(f"文件未找到: {file_path}")
                continue
                
            try:
                key, url = await self._get_url(file_path)
                book_links.append((book_dict, url))
            except Exception as e:
                logger.error(f"文件{file_path}上传失败: {str(e)}")

        # 设置邮件正文
        if book_links:
            body = message or self._generate_books_email_body_with_urls(book_links)
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            return msg
        else:
            logger.error("没有书籍需要发送")
            raise ValueError("没有书籍需要发送")

    def _generate_book_email_body(self, book_dict: dict) -> str:
        """生成单本书籍的邮件正文"""
        book_title = book_dict.get('title', '')
        file_size = book_dict.get('file_size', 0)
        return f"""
        您好，

        已为您附上《{book_title}》。

        书籍详情：
        - 标题：{book_title}
        - 文件大小：{file_size / 1024 / 1024:.2f}MB

        祝您阅读愉快！
        
        ----
        由 Book Sender 自动发送
        """

    def _generate_book_email_body_with_url(self, book_dict: dict, url: str) -> str:
        """生成带下载链接的邮件正文"""
        book_title = book_dict.get('title', '')
        file_size = book_dict.get('file_size', 0)
        return f"""
        您好，

        已为您准备《{book_title}》。

        书籍详情：
        - 标题：{book_title}
        - 文件大小：{file_size / 1024 / 1024:.2f}MB

        下载链接：
        {url}

        注意：此链接将在7天后过期，请及时下载。

        祝您阅读愉快！
        """

    def _generate_books_email_body_with_urls(self, book_links: List[Tuple[dict, str]]) -> str:
        """生成带下载链接的多本书籍邮件正文"""
        books_info = []
        for book_dict, url in book_links:
            book_title = book_dict.get('title', '')
            file_size = book_dict.get('file_size', 0)
            books_info.append(f"""
        《{book_title}》
        - 文件大小：{file_size / 1024 / 1024:.2f}MB
        - 下载链接：{url}""")

        return f"""
        您好，

        已为您准备以下书籍：

        {''.join(books_info)}

        注意：下载链接将在7天后过期，请及时下载。

        祝您阅读愉快！
        """
