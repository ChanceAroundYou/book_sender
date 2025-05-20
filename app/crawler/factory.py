from typing import Type, overload, Literal

from app.crawler.base import BaseCrawler
from app.crawler.economist_crawler import EconomistCrawler

@overload
def create_crawler(crawler_type: Literal['economist'], *args, **kwargs) -> EconomistCrawler:
    ...

def create_crawler(crawler_type: str, *args, **kwargs) -> BaseCrawler:
    """创建爬虫实例
    
    Args:
        crawler_type: 爬虫类型，支持 'economist'
        
    Returns:
        BaseCrawler: 爬虫实例，具体类型取决于 crawler_type
    """
    crawler_map: dict[str, Type[BaseCrawler]] = {
        'economist': EconomistCrawler,
    }
    if crawler_type not in crawler_map:
        raise ValueError(f"Unsupported crawler type: {crawler_type}")

    return crawler_map[crawler_type](*args, **kwargs)