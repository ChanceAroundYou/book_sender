import logging
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio

from app.config import settings
from app.crawler.economist_crawler import EconomistCrawler
from app.downloader.economist_downloader import FileDownloader

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@pytest_asyncio.fixture
async def crawler() -> AsyncGenerator[EconomistCrawler, None]:
    """创建爬虫实例的 fixture"""
    async with EconomistCrawler() as crawler:
        yield crawler


@pytest.mark.asyncio
async def test_get_books(crawler: EconomistCrawler):
    """测试获取杂志列表"""
    book_dicts = await crawler.get_books(page=1)
    assert book_dicts is not None
    assert len(book_dicts) > 0

    # 验证每本书的基本信息
    for book_dict in book_dicts:
        assert book_dict["title"] is not None
        assert book_dict["detail_link"] is not None
        assert book_dict["date"] is not None
        assert book_dict["cover_link"] is not None


@pytest.mark.asyncio
async def test_get_book(crawler: EconomistCrawler):
    """测试获取单本杂志详情"""
    # 先获取杂志列表
    book_dicts = await crawler.get_books(page=1)
    assert len(book_dicts) > 0

    # 获取第一本杂志的详情
    book_dict = await crawler.get_book(book_dicts[0])
    assert book_dict is not None
    assert book_dict["download_link"] is not None


@pytest.mark.asyncio
async def test_download_book(crawler: EconomistCrawler):
    """测试下载杂志"""
    # 设置临时下载目录
    download_dir = settings.TMP_DIR / "downloads"
    download_dir.mkdirs(exist_ok=True)

    # 获取杂志列表和详情
    book_dicts = await crawler.get_books(page=1)
    assert len(book_dicts) > 0
    book_dict = await crawler.get_book(book_dicts[0])
    assert book_dict["download_link"] is not None

    # 下载杂志
    downloader = FileDownloader()
    book_dict = await downloader.download_book(book_dict)

    # 验证下载结果
    assert book_dict["file_path"] is not None
    assert Path(book_dict["file_path"]).exists()
    assert Path(book_dict["file_path"]).is_file()


@pytest.mark.asyncio
async def test_crawler_integration(crawler: EconomistCrawler):
    """测试爬虫完整流程"""
    # 设置临时下载目录
    download_dir = settings.TMP_DIR / "downloads"
    download_dir.mkdirs(exist_ok=True)

    # 1. 获取杂志列表
    book_dicts = await crawler.get_books(page=1)
    assert len(book_dicts) > 0

    # 2. 获取第一本杂志的详情
    book_dict = await crawler.get_book(book_dicts[0])
    assert book_dict["download_link"] is not None

    # 3. 下载杂志
    downloader = FileDownloader()
    book_dict = await downloader.download_book(book_dict)

    # 4. 验证结果
    assert book_dict["file_path"] is not None
    assert Path(book_dict["file_path"]).exists()
    assert Path(book_dict["file_path"]).is_file()
