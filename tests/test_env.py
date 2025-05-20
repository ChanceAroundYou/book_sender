from app.config import settings


def test_database_config():
    """测试数据库配置是否正确加载"""
    assert settings.POSTGRES_SERVER is not None
    assert settings.POSTGRES_USER is not None
    assert settings.POSTGRES_PASSWORD is not None
    assert settings.POSTGRES_DB is not None
    assert settings.SQLALCHEMY_DATABASE_URI is not None


def test_redis_config():
    """测试Redis配置是否正确加载"""
    assert settings.REDIS_HOST is not None
    assert isinstance(settings.REDIS_PORT, int)
    assert isinstance(settings.REDIS_DB, int)
    assert settings.CELERY_BROKER_URL.startswith("redis://")
    assert settings.CELERY_RESULT_BACKEND.startswith("redis://")


def test_aws_config():
    """测试AWS配置是否正确加载"""
    assert settings.AWS_REGION is not None
    assert settings.AWS_S3_BUCKET is not None
    assert settings.AWS_S3_ENDPOINT_URL is not None


def test_email_config():
    """测试邮件配置是否正确加载"""
    assert settings.SMTP_SERVER is not None
    assert isinstance(settings.SMTP_PORT, int)
    assert settings.SMTP_USERNAME is not None
    assert settings.SMTP_SENDER_EMAIL is not None


def test_storage_config():
    """测试存储配置是否正确加载"""
    assert settings.STORAGE_PROVIDER in ["s3", "r2"]
    if settings.STORAGE_PROVIDER == "r2":
        assert settings.R2_ACCESS_KEY_ID is not None
        assert settings.R2_SECRET_ACCESS_KEY is not None
        assert settings.R2_ENDPOINT_URL is not None
        assert settings.R2_BUCKET is not None
    else:
        assert settings.AWS_ACCESS_KEY_ID is not None
        assert settings.AWS_SECRET_ACCESS_KEY is not None
