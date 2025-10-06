from typing import Literal, Type, overload

from app.downloader.base import BaseDownloader
from app.downloader.economist_downloader import FileDownloader

# @overload
# def create_downloader(downloader_type: Literal['file'], *args, **kwargs) -> FileDownloader:
    ...

def create_downloader(downloader_type: str, *args, **kwargs) -> BaseDownloader:
    """创建下载器实例
    
    Args:
        downloader_type: 下载器类型，支持 'file'
        
    Returns:
        BaseDownloader: 下载器实例，具体类型取决于 downloader_type
    """
    downloader_map: dict[str, Type[BaseDownloader]] = {
        'file': FileDownloader,
    }
    if downloader_type not in downloader_map:
        raise ValueError(f"Unsupported downloader type: {downloader_type}")

    return downloader_map[downloader_type](*args, **kwargs)