# 加载环境变量
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


def load_env_file(env_file: Optional[str] = None) -> None:
    """加载环境变量文件
    
    Args:
        env_file: 环境变量文件路径，如果为 None，则按以下顺序查找：
                 1. .env.local
                 2. .env
    """
    if env_file:
        # 如果指定了文件，直接加载
        load_dotenv(env_file)
        return

    # 获取项目根目录
    root_dir = Path(__file__).parent.parent
    
    # 按优先级查找环境变量文件
    env_files = [
        root_dir / '.env.local',  # 本地开发环境
        root_dir / '.env',        # 默认环境
    ]
    
    # 加载找到的第一个环境变量文件
    for env_path in env_files:
        if env_path.exists():
            load_dotenv(env_path)
            print(f"已加载环境变量文件: {env_path}")
            return
            
    print("警告: 未找到环境变量文件，将使用默认值") 

load_env_file()

class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "Book Sender"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # 安全配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # 数据库配置
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Redis配置
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = 0
    
    # 文件存储配置
    BOOKS_DIR: str = "app/static/books"
    MAX_BOOK_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # 爬虫配置
    CRAWLER_DELAY: int = 3  # 爬虫延迟（秒）
    MAX_RETRIES: int = 3    # 最大重试次数
    
    # 分发器配置
    MAX_DOWNLOAD_CONCURRENT: int = 5  # 最大并发下载数
    DOWNLOAD_SPEED_LIMIT: int = 1024 * 1024  # 1MB/s

    # 下载配置
    DOWNLOAD_DIR: str = "downloads"

    # Celery配置
    CELERY_BROKER_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    CELERY_RESULT_BACKEND: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    CELERY_TASK_MAX_RETRIES: int = 3

    # Email settings
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_SENDER_EMAIL: str = os.getenv("SMTP_SENDER_EMAIL", "")

    # AWS Settings
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-northeast-1")
    
    # Email Settings
    EMAIL_BACKEND: str = os.getenv("EMAIL_BACKEND", "ses")  # smtp or ses
    SES_EMAIL_SENDER: str = os.getenv("SES_EMAIL_SENDER", "")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True  # 区分大小写
        env_file_encoding = 'utf-8'  # 确保正确的文件编码

settings = Settings() 