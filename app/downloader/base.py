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
        self.download_dir.mkdir(exist_ok=True, parents=True)
        self.headers = {
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

    async def _check_downloading(self, file_path: Path, check_interval: int = 15) -> bool:
        """检查文件是否正在下载中"""
        if not file_path.exists():
            return False
        
        initial_size = os.path.getsize(file_path)
        logger.info(f"检测到已存在文件: {file_path}，大小: {initial_size} 字节。")
        if initial_size == 0:
            logger.info("文件大小为0，不在下载")
            return False

        logger.info(f"监测文件大小 {check_interval} 秒...")
        await asyncio.sleep(check_interval)
        new_size = os.path.getsize(file_path)

        if new_size == initial_size:
            logger.info("文件在监测期间未变化，不在下载")
            return False

        logger.info(f"文件大小: {initial_size} -> {new_size}，正在下载")
        return True

    async def download_book(self, book_dict: dict) -> dict:
        """下载文件并返回文件信息"""
        if not (download_link := book_dict.get("download_link", "")):
            logger.error(f"下载链接为空: {book_dict.get('title', '')}")
            return book_dict

        if not (file_format := BookFormat.get_format(download_link)):
            logger.error(f"未知的文件类型: {download_link}")
            return book_dict

        file_name = f"{book_dict.get('title', '')}.{file_format}"
        file_path = self.download_dir / file_name
        
        if await self._check_downloading(file_path):
            logger.info(f"文件正在下载，跳过下载: {file_path}")
            return book_dict

        logger.info(f"开始下载: {file_name}")

        try:
            response = requests.get(download_link, headers=self.headers, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            with open(file_path, "wb") as f:
                chunk_size = 128 * 1024
                last_tm = datetime.now(UTC)
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if not chunk:
                        continue

                    f.write(chunk)
                    now_tm = datetime.now(UTC)
                    if (now_tm - last_tm).seconds >= 10:
                        logger.debug(f"{file_name}进度: {f.tell()/total_size*100:.2f}%, {f.tell()/1024/1024:.2f}/{total_size/1024/1024:.2f} MB")
                        last_tm = now_tm

            logger.info(f"下载完成: {file_path}")

            book_dict["downloaded_at"] = datetime.now(UTC)
            book_dict["file_path"] = str(file_path)
            book_dict["file_size"] = total_size
            book_dict["file_format"] = file_format
            return book_dict

        except Exception as e:
            logger.error(f"下载失败: {str(e)}")
            file_path.unlink(missing_ok=True)
            raise e
