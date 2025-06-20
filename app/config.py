# 加载环境变量
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from loguru import logger
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
        root_dir / ".env.local",  # 本地开发环境
        root_dir / ".env",  # 默认环境
    ]

    # 加载找到的第一个环境变量文件
    for env_path in env_files:
        if env_path.exists():
            load_dotenv(env_path)
            logger.info(f"加载环境变量文件: {env_path}")
            return


load_env_file()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Book Sender"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://192.168.1.10:3000",
        "http://192.168.1.10:3001",
        "http://192.168.1.10:5173",
        "http://192.168.1.6:3000",
        "http://192.168.1.6:3001",
        "http://192.168.1.6:5173",
        "http://192.168.1.6:25688",
        "http://localhost:8000",
        "http://localhost:25688",
        "http://192.168.1.6:8000",
        "http://192.168.1.6:25688",
        "https://book.xiaokubao.space",
        "https://book.xiaokubao.cloud",
        "https://home.xiaokubao.space",
        "https://book.pages.dev",
        "https://booksender.pages.dev",
        "https://booksender.xiaokubao.space",
        "https://booksender.xiaokubao.cloud",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    CORS_ALLOW_HEADERS: list = [
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
    ]

    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # 数据库配置
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
    SQLITE_DB_FILENAME: str = "app.db"  # Default SQLite filename
    CELERY_DB_FILENAME: str = "celery.db"  # Default Celery SQLite filename
    DB_DIR: str = os.getenv("DB_DIR", "app/db")
    SQLITE_DB_FILENAME: str = "app.db"
    CELERY_DB_FILENAME: str = "celery.db"
    CELERY_BEAT_SCHEDULE_FILENAME: str = (
        "celerybeat-schedule.sqlite3"  # For dedicated beat schedule DB
    )

    # Common SQLite PRAGMA settings for optimization
    SQLITE_OPTIMIZATIONS: str = "?journal_mode=WAL&busy_timeout=5000&synchronous=NORMAL"
    # For main app DB, consider synchronous=FULL for max safety:
    # SQLITE_MAIN_DB_OPTIMIZATIONS: str = "?journal_mode=WAL&busy_timeout=5000&synchronous=FULL"

    @property
    def DATABASE_URL(self) -> str:
        # db_dir = Path(self.DB_DIR)
        # db_dir.mkdir(parents=True, exist_ok=True)
        # db_path = (db_dir / self.SQLITE_DB_FILENAME).resolve()
        # return f"sqlite:///{db_path}{self.SQLITE_OPTIMIZATIONS}"
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    # Redis配置
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = 0

    # 文件存储配置

    DOWNLOAD_DIR: str = os.getenv("DOWNLOAD_DIR", "downloads")
    MAX_BOOK_SIZE: int = 100 * 1024 * 1024

    # 爬虫配置
    CRAWLER_DELAY: int = 3  # 爬虫延迟（秒）
    MAX_RETRIES: int = 3  # 最大重试次数

    # 分发器配置
    MAX_DOWNLOAD_CONCURRENT: int = 5  # 最大并发下载数
    DOWNLOAD_SPEED_LIMIT: int = 1024 * 1024  # 1MB/s
    DISTRIBUTOR_TYPE: str = "smtp"

    # Download settings
    DOWNLOADER_TYPE: str = "file"

    # Uploader settings
    UPLOADER_TYPE: str = "r2"

    # Celery configuration
    CELERY_WORKER_CONCURRENCY: int = os.getenv("CELERY_WORKER_CONCURRENCY", 4)
    CELERY_WORKER_PREFETCH_MULTIPLIER: int = os.getenv(
        "CELERY_WORKER_PREFETCH_MULTIPLIER", 4
    )

    @property
    def CELERY_BROKER_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    CELERY_TASK_MAX_RETRIES: int = 3

    # Email settings
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "465"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_SENDER_EMAIL: str = os.getenv("SMTP_SENDER_EMAIL", "")
    # Email Settings
    SES_EMAIL_SENDER: str = os.getenv("SES_EMAIL_SENDER", "")
    # AWS Settings
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-northeast-1")

    AWS_S3_BUCKET: str = os.getenv("AWS_S3_BUCKET", "book-sender")
    AWS_S3_ENDPOINT_URL: str = os.getenv("AWS_S3_ENDPOINT_URL", "")
    # Cloudflare R2 Settings
    R2_ACCESS_KEY_ID: str = os.getenv("R2_ACCESS_KEY_ID", "")
    R2_SECRET_ACCESS_KEY: str = os.getenv("R2_SECRET_ACCESS_KEY", "")
    R2_ENDPOINT_URL: str = os.getenv("R2_ENDPOINT_URL", "")
    R2_BUCKET: str = os.getenv("R2_BUCKET", "book-sender")

    # Storage Provider
    STORAGE_PROVIDER: str = os.getenv("STORAGE_PROVIDER", "s3")  # s3 or r2


settings = Settings()
