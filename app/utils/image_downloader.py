import hashlib
import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx
from loguru import logger

from app.config import settings


class ImageDownloader:
    def __init__(self):
        self.img_dir = settings.STATIC_DIR / "images"
        self.img_dir.mkdirs(exist_ok=True)

    def _get_file_extension(self, url: str, content_type: str = None) -> str:
        """从URL或Content-Type中获取文件扩展名"""
        # 从URL中提取扩展名
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()

        # 常见的图片扩展名
        image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"]

        for ext in image_extensions:
            if path.endswith(ext):
                return ext

        # 从Content-Type中推断扩展名
        if content_type:
            content_type = content_type.lower()
            if "jpeg" in content_type or "jpg" in content_type:
                return ".jpg"
            elif "png" in content_type:
                return ".png"
            elif "gif" in content_type:
                return ".gif"
            elif "webp" in content_type:
                return ".webp"
            elif "svg" in content_type:
                return ".svg"

        # 默认返回.jpg
        return ".jpg"

    def _generate_filename(self, title: str, url: str) -> str:
        """生成文件名"""
        # 清理标题，移除特殊字符
        clean_title = re.sub(r"[^\w\s-]", "", title)
        clean_title = re.sub(r"[-\s]+", "-", clean_title).strip("-")

        # 使用URL的哈希值确保唯一性
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]

        return f"{clean_title}_{url_hash}"

    async def download_image(self, url: str, title: str) -> Optional[str]:
        """下载图片并返回保存路径"""
        if not url:
            logger.warning("图片URL为空")
            return None

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers, follow_redirects=True)
                response.raise_for_status()

                # 检查Content-Type
                content_type = response.headers.get("content-type", "")
                if not content_type.startswith("image/"):
                    logger.warning(f"URL返回的不是图片: {content_type}")
                    return None

                # 生成文件名和路径
                filename = self._generate_filename(title, url)
                extension = self._get_file_extension(url, content_type)
                file_path = self.img_dir / f"{filename}{extension}"

                # 如果文件已存在，直接返回路径
                if file_path.exists():
                    logger.info(f"图片已存在: {file_path}")
                    return str(file_path)

                # 保存图片
                with open(file_path, "wb") as f:
                    f.write(response.content)

                logger.info(f"图片下载成功: {file_path}")
                return str(file_path)

        except httpx.TimeoutException:
            logger.error(f"下载图片超时: {url}")
        except httpx.RequestError as e:
            logger.error(f"下载图片请求错误: {url}, 错误: {e}")
        except Exception as e:
            logger.error(f"下载图片失败: {url}, 错误: {e}")

        return None
