from app.config import settings
from app.uploader.s3 import S3Uploader


class R2Uploader(S3Uploader):
    """Cloudflare R2 上传器"""

    uploader_type = "r2"

    def __init__(self):
        # 创建带有重试配置的 R2 客户端
        self.region = "auto"
        self.bucket_name = settings.R2_BUCKET
        self.access_key_id = settings.R2_ACCESS_KEY_ID
        self.secret_access_key = settings.R2_SECRET_ACCESS_KEY
        self.endpoint_url = settings.R2_ENDPOINT_URL
        self.build_client()

    # def build_client(self):
    #     """重写 build_client 方法以正确配置 R2 客户端"""
    #     config = Config(
    #         region_name=self.region,
    #         retries={
    #             'max_attempts': 3,
    #             'mode': 'adaptive'
    #         },
    #         connect_timeout=10,
    #         read_timeout=60,
    #         max_pool_connections=10,
    #         tcp_keepalive=True
    #     )
    #     self.client = boto3.client(
    #         's3',
    #         aws_access_key_id=self.access_key_id,
    #         aws_secret_access_key=self.secret_access_key,
    #         region_name=self.region,
    #         endpoint_url=self.endpoint_url,
    #         config=config
    #     )

    #     self._ensure_bucket_exists()
