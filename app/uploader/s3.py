import os
from typing import Any, Dict, List
from urllib.parse import quote

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from loguru import logger

from app.config import settings
from app.uploader.base import BaseUploader


class S3Uploader(BaseUploader):
    """AWS S3 上传器"""
    uploader_type = "s3"
    
    def __init__(self):
        # 创建带有重试配置的 S3 客户端
        self.region = settings.AWS_REGION
        self.bucket_name = settings.AWS_S3_BUCKET
        self.access_key_id = settings.AWS_ACCESS_KEY_ID
        self.secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        self.endpoint_url = settings.AWS_S3_ENDPOINT_URL
        self.build_client()
    
    def build_client(self):
        config = Config(
            region_name=self.region,
            retries={
                'max_attempts': 3,
                'mode': 'adaptive'
            },
            # 上传大文件的配置
            connect_timeout=10,
            read_timeout=60,
            max_pool_connections=10,
            tcp_keepalive=True
        )
        self.client = boto3.client(
            's3',
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region,
            endpoint_url=self.endpoint_url,
            config=config
        )
        
        
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """确保 bucket 存在，如果不存在则创建"""
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"bucket '{self.bucket_name}' 已存在")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.info(f"正在创建 bucket '{self.bucket_name}'...")
                self.client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': self.region
                    }
                )
                logger.info(f"bucket '{self.bucket_name}' 创建成功")
            else:
                raise
    
    def upload_file(self, file_path: str, key: str | None = None) -> str:
        """上传文件到
        
        Args:
            file_path: 本地文件路径
            key: 文件键名，如果不指定则使用文件名
            
        Returns:
            str: 文件键名
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 如果没有指定key，使用文件名作为key
        if key is None:
            key = os.path.basename(file_path)
        
        try:
            logger.debug(f"正在上传文件 {file_path} 到 bucket '{self.bucket_name}'...")
            self.client.upload_file(file_path, self.bucket_name, key)
            logger.info(f"文件上传成功: s3://{self.bucket_name}/{key}")
            return key
        except ClientError as e:
            logger.error(f"文件上传失败: {str(e)}")
            raise
    
    def generate_url(self, key: str, expires_in: int = 604800) -> str:
        """生成预签名URL
        
        Args:
            key: 文件键名
            expires_in: URL有效期（秒），默认7天
            
        Returns:
            str: 预签名URL
        """
        try:
            # 对文件名进行URL编码
            filename = os.path.basename(key)
            encoded_filename = quote(filename)
            
            # 生成预签名URL
            url = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': key,
                    'ResponseContentDisposition': f'attachment; filename="{encoded_filename}"'
                },
                ExpiresIn=expires_in
            )
            
            logger.debug(f"生成预签名URL成功: {url}")
            return url
        except ClientError as e:
            logger.error(f"生成预签名URL失败: {str(e)}")
            raise
    
    def file_exists(self, key: str) -> bool:
        """检查文件是否存在
        
        Args:
            key: 文件键名
            
        Returns:
            bool: 文件是否存在
        """
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise
    
    def get_file_info(self, key: str) -> Dict[str, Any]:
        """获取文件信息
        
        Args:
            key: 文件键名
            
        Returns:
            Dict[str, Any]: 文件信息，包含大小、最后修改时间等
        """
        try:
            response = self.client.head_object(Bucket=self.bucket_name, Key=key)
            return {
                'key': key,
                'size': response['ContentLength'],
                'last_modified': response['LastModified'],
                'content_type': response.get('ContentType'),
                'etag': response['ETag'].strip('"'),
                'metadata': response.get('Metadata', {})
            }
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise FileNotFoundError(f"文件不存在: {key}")
            raise
    
    def list_files(self, prefix: str | None = None) -> List[Dict[str, Any]]:
        """列出文件
        
        Args:
            prefix: 文件前缀，用于过滤
            
        Returns:
            List[Dict[str, Any]]: 文件列表，每个文件包含键名、大小、最后修改时间等信息
        """
        try:
            files = []
            paginator = self.client.get_paginator('list_objects_v2')
            
            # 构建请求参数
            params = {'Bucket': self.bucket_name}
            if prefix is not None:
                params['Prefix'] = prefix
            
            for page in paginator.paginate(**params):
                if 'Contents' not in page:
                    continue
                    
                for obj in page['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'],
                        'etag': obj['ETag'].strip('"')
                    })
            
            return files
        except ClientError as e:
            logger.error(f"列出文件失败: {str(e)}")
            raise
    
    def delete_file(self, key: str) -> bool:
        """删除文件
        
        Args:
            key: 文件键名
            
        Returns:
            bool: 是否删除成功
        """
        try:
            # 先检查文件是否存在
            if not self.file_exists(key):
                return False
                
            self.client.delete_object(Bucket=self.bucket_name, Key=key)
            logger.info(f"文件删除成功: s3://{self.bucket_name}/{key}")
            return True
        except ClientError as e:
            logger.error(f"文件删除失败: {str(e)}")
            return False
    
    def delete_files(self, keys: List[str]) -> Dict[str, bool]:
        """批量删除文件
        
        Args:
            keys: 文件键名列表
            
        Returns:
            Dict[str, bool]: 每个文件的删除结果
        """
        if not keys:
            return {}
            
        try:
            # 将文件列表分成每1000个一组（S3 API限制）
            results = {}
            for i in range(0, len(keys), 1000):
                batch = keys[i:i + 1000]
                response = self.client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={
                        'Objects': [{'Key': key} for key in batch],
                        'Quiet': False
                    }
                )
                
                # 处理删除结果
                for deleted in response.get('Deleted', []):
                    results[deleted['Key']] = True
                for error in response.get('Errors', []):
                    results[error['Key']] = False
                    logger.error(f"删除文件失败: {error['Key']}, 原因: {error['Message']}")
            
            return results
        except ClientError as e:
            logger.error(f"批量删除文件失败: {str(e)}")
            raise
