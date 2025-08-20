import asyncio
import os
import random
from datetime import UTC, datetime
from pathlib import Path

import requests
from loguru import logger

from app.config import settings
from app.database.book import BookFormat


class BaseDownloader:
    def __init__(self):
        self.download_dir: Path = settings.DOWNLOAD_DIR
        self.download_dir.mkdirs(exist_ok=True)

    async def delay(self, min_seconds=1, max_seconds=3):
        """异步延迟"""
        delay_time = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay_time)

    async def download_book(self, book_dict: dict) -> dict:
        """下载文件并返回文件信息"""
        download_link = book_dict.get("download_link", "")
        if not download_link:
            logger.error(f"下载链接为空: {book_dict.get('title', '')}")
            return book_dict

        if ".pdf" in download_link:
            file_format = BookFormat.PDF
        elif ".epub" in download_link:
            file_format = BookFormat.EPUB
        elif ".mobi" in download_link:
            file_format = BookFormat.MOBI
        elif ".txt" in download_link:
            file_format = BookFormat.TXT
        else:
            logger.error(f"未知的文件类型: {download_link}")
            return book_dict

        file_name = f"{book_dict.get('title', '')}.{file_format}"
        logger.info(f"正在下载: {file_name}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }

        try:
            response = requests.get(download_link, headers=headers, stream=True)
            response.raise_for_status()

            file_path = os.path.join(self.download_dir, file_name)
            total_size = int(response.headers.get("content-length", 0))
            with open(file_path, "wb") as f:
                chunk_size = 128 * 1024
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)

            logger.info(f"下载完成: {file_path}")

            book_dict["downloaded_at"] = datetime.now(UTC)
            book_dict["file_path"] = file_path
            book_dict["file_size"] = total_size
            book_dict["file_format"] = file_format
            return book_dict

        except Exception as e:
            logger.error(f"下载失败: {str(e)}")
            os.remove(file_path)
            raise e
