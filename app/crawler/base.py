import asyncio
import random
from typing import List


class BaseCrawler:
    def __init__(self,base_url=''):
        self.base_url = base_url

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.close()

    async def delay(self, min_seconds=1, max_seconds=3):
        """异步延迟"""
        delay_time = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay_time)

    async def get(self, url):
        raise NotImplementedError

    async def get_books(self, page: int = 1) -> List[dict]:
        raise NotImplementedError

    async def get_book(self, book_dict: dict) -> dict:
        raise NotImplementedError
    
    async def close(self):
        pass
