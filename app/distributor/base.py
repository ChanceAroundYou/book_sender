import os
from abc import ABC, abstractmethod
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from loguru import logger

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

class BaseDistributor(ABC):
    """分发器基类，定义分发器接口"""

    def __init__(self, sender_email: str):
        self.sender_email = sender_email

    @abstractmethod
    async def send_book(self, 
                       book_dict: dict, 
                       email: str,
                       subject: Optional[str] = None,
                       message: Optional[str] = None) -> bool:
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
                        subject: Optional[str] = None,
                        message: Optional[str] = None) -> bool:
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

    def create_book_email(self, 
                         book_dict: dict,
                         email: str,
                         subject: Optional[str] = None,
                         message: Optional[str] = None) -> MIMEMultipart:
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

        msg = MIMEMultipart()
        msg['Subject'] = subject or f"发送书籍：《{book_title}》"
        msg['From'] = f"Book Sender <{self.sender_email}>"
        msg['To'] = email

        body = message or self._generate_book_email_body(book_dict)
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        if file_path and os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                mime_subtype = get_mime_subtype(file_format)
                book_file = MIMEApplication(f.read(), _subtype=mime_subtype)
                filename = os.path.basename(file_path)
                book_file.add_header('Content-Disposition', 'attachment', 
                                   filename=('utf-8', '', filename))
                msg.attach(book_file)
        else:
            logger.warning(f"文件未找到: {file_path}")

        return msg

    def create_books_email(self,
                          book_dicts: List[dict],
                          email: str,
                          subject: Optional[str] = None,
                          message: Optional[str] = None) -> MIMEMultipart:
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

        # 设置邮件正文
        body = message or self._generate_books_email_body(book_dicts)
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 添加所有附件
        for book_dict in book_dicts:
            file_path = book_dict.get('file_path', '')
            file_format = book_dict.get('file_format', '')
            
            if file_path and os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    mime_subtype = get_mime_subtype(file_format)
                    book_file = MIMEApplication(f.read(), _subtype=mime_subtype)
                    filename = os.path.basename(file_path)
                    book_file.add_header('Content-Disposition', 'attachment', 
                                       filename=('utf-8', '', filename))
                    msg.attach(book_file)
            else:
                logger.warning(f"文件未找到: {file_path}")

        return msg

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

    def _generate_books_email_body(self, book_dicts: List[dict]) -> str:
        """生成多本书籍的邮件正文"""
        book_list = "\n".join([
            f"- 《{book_dict.get('title', '')}》（{book_dict.get('file_size', 0) / 1024 / 1024:.2f}MB）"
            for book_dict in book_dicts
        ])
        
        return f"""
        您好，

        已为您附上{len(book_dicts)}本书籍：

        {book_list}

        祝您阅读愉快！
        
        ----
        由 Book Sender 自动发送
        """
