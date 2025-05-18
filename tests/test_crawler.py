import asyncio
import logging

from app.crawler.economist_crawler import EconomistCrawler
from app.downloader.economist_downloader import EconomistDownloader

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_crawler():
    """测试爬虫功能 (异步 Playwright 版)"""
    try:
        async with EconomistCrawler() as crawler:
            print("\n测试获取杂志列表...")
            books = await crawler.get_books(page=1)
            print(f"找到 {len(books)} 期杂志")
            if books:
                print("\n杂志列表:")
                for book in books:
                    print(f"标题: {book.title}")
                    print(f"链接: {book.detail_link}")
                    print(f"日期: {book.date}")
                    print(f"封面图：{book.cover_link}")
                    print("-" * 50)

                print("\n测试获取下载链接...")
                book = books[0]
                book = await crawler.get_book(book)
                print(f"下载链接: {book.download_link}")
                if book.download_link:
                    print("\n测试下载杂志...")
                    downloader = EconomistDownloader()
                    book = downloader.download_book(book)
                    if book.file_path:
                        print(f"成功下载: {book.title}")
                        print(f"文件路径: {book.file_path}")

    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(test_crawler()) 