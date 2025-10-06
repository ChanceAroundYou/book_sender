from typing import Type, overload, Literal

from app.uploader.base import BaseUploader
from app.uploader.r2 import R2Uploader
from app.uploader.s3 import S3Uploader

# @overload
# def create_uploader(uploader_type: Literal['r2'], *args, **kwargs) -> R2Uploader:
#     ...

# @overload
# def create_uploader(uploader_type: Literal['s3'], *args, **kwargs) -> S3Uploader:
#     ...

def create_uploader(uploader_type: str, *args, **kwargs) -> BaseUploader:
    """创建上传器实例
    
    Args:
        uploader_type: 上传器类型，支持 'r2' 或 's3'
        *args: 位置参数
        **kwargs: 关键字参数
        
    Returns:
        BaseUploader: 上传器实例，具体类型取决于 uploader_type
    """
    uploader_map: dict[str, Type[BaseUploader]] = {
        'r2': R2Uploader,
        's3': S3Uploader,
    }
    if uploader_type not in uploader_map:
        raise ValueError(f"Unsupported uploader type: {uploader_type}")

    return uploader_map[uploader_type](*args, **kwargs)