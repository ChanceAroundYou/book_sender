from typing import Type, TypeVar

from app.downloader.base import BaseDownloader
from app.downloader.economist_downloader import EconomistDownloader

T = TypeVar('T', bound=BaseDownloader)

def create_downloader(downloader_type: str, *args, **kwargs) -> T:
    """创建下载器实例
    
    Args:
        downloader_type: 下载器类型，支持 'economist'
        
    Returns:
        BaseDownloader: 下载器实例，具体类型取决于 downloader_type
    """
    downloader_map: dict[str, Type[T]] = {
        'economist': EconomistDownloader,
    }
    if downloader_type not in downloader_map:
        raise ValueError(f"Unsupported downloader type: {downloader_type}")

    return downloader_map[downloader_type](*args, **kwargs)