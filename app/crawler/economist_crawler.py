import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from loguru import logger
from playwright.async_api import async_playwright

from app.config import settings
from app.crawler.base import BaseCrawler
from app.utils.image_downloader import ImageDownloader
from app.utils.image_processor import ImageProcessor


class EconomistCrawler(BaseCrawler):
    def __init__(self, base_url="https://magazinelib.com/all/the-economist/page/{}/"):
        super().__init__(base_url)
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.image_processor = ImageProcessor(debug=False)
        self.image_downloader = ImageDownloader()
        self.series_name = "the-economist"
        logger.info(f"Initialized crawler for series: {self.series_name}")

    async def __aenter__(self):
        """Async context manager entry"""
        await self.init_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    async def init_browser(self):
        """Initialize Playwright browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            # headless=False,
            # executable_path='/usr/bin/chromium-browser',
            args=["--no-sandbox"],
        )
        self.context = await self.browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        self.page = await self.context.new_page()

    async def _find_and_click_checkbox(self, is_saved: bool = False) -> bool:
        """查找并点击 checkbox"""
        if not self.page:
            raise RuntimeError("Browser not initialized")

        screenshot_path = await self._take_screenshot()
        # 在图像中查找 checkbox
        checkbox_pos = self.image_processor.find_checkbox(screenshot_path)
        # 删除截图文件
        if not is_saved and os.path.exists(screenshot_path):
            # logger.info(f"Delete screenshot: {screenshot_path}")
            os.remove(screenshot_path)
        else:
            logger.info(f"Save screenshot: {screenshot_path}")

        if checkbox_pos:
            # 如果找到 checkbox，点击它
            x, y = checkbox_pos
            x += random.randint(-5, 5)
            y += random.randint(-5, 5)
            await self.page.mouse.click(x, y)
            logger.info(f"Click Cloudflare checkbox ({x}, {y})")
            await self.delay(1, 3)
            return True
        else:
            # logger.info("未找到 checkbox")
            return False

    async def _take_screenshot(self, save_dir: Path = settings.TMP_DIR / "screenshot"):
        """Get full page screenshot"""
        # 创建保存目录
        if not self.page:
            raise RuntimeError("Browser not initialized")

        save_dir.mkdir(exist_ok=True, parents=True)
        now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        screenshot_path = save_dir / f"{now}_{random.randint(1, 50):02d}_full.png"

        # 使用 Playwright 截图
        await self.page.screenshot(path=screenshot_path)
        return screenshot_path

    async def get(
        self, url, max_wait_time=settings.MAX_WAIT_TIME, loaded_selector=None
    ):
        """Get page safely, handling Cloudflare verification and other issues"""

        if not self.page:
            raise RuntimeError("Browser not initialized")

        logger.info(f"Get page: {url}")
        await self.page.goto(url)
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            try:
                if "Just a moment" in await self.page.title():
                    # await self.delay(5, 10)
                    if not await self._find_and_click_checkbox():
                        await self.delay(5, 10)
                        continue
                    else:
                        await self.delay(5, 10)

                if loaded_selector is not None:
                    loaded_element = await self.page.query_selector(loaded_selector)
                    if loaded_element:
                        content = await self.page.content()
                        return BeautifulSoup(content, "html.parser")
                else:
                    content = await self.page.content()
                    return BeautifulSoup(content, "html.parser")
            except Exception as e:
                logger.error(f"Error occurred while getting page content: {e}")
            # 随机延迟后继续检测
            await self.delay(1, 2)
        # 超时抛出异常
        raise TimeoutError(f"Timeout for {max_wait_time}s to load {url}")

    async def get_books(self, page: int = 1) -> List[dict]:
        url = self.base_url.format(page)
        soup = await self.get(url, loaded_selector="div#page")

        book_elements = soup.find_all("article", class_="category-all")

        book_dicts = []
        for book_element in book_elements:
            title_element = book_element.find("h3", class_="entry-title")
            title = title_element.text.strip()
            link_element = title_element.find("a")
            detail_link = link_element["href"]
            date_element = book_element.find("time", class_="entry-date")
            date = date_element.text.strip() if date_element else None
            if date:
                date = datetime.strptime(date, "%d.%m.%Y, %H:%M").strftime("%Y-%m-%d")

            cover_element = book_element.find("img", class_="wp-post-image")
            cover_link = (
                cover_element["data-src"]
                if cover_element and "data-src" in cover_element.attrs
                else None
            )

            book_dict = {
                "title": title,
                "date": date,
                "series": self.series_name,
                "detail_link": detail_link,
                "cover_link": cover_link,
            }

            book_dicts.append(book_dict)
        logger.info(f"Found {len(book_dicts)} issues on page {page}")
        return book_dicts

    async def get_book(self, book_dict: dict) -> dict:
        logger.info(f"Getting book details: {book_dict['title']}")
        soup = await self.get(book_dict["detail_link"], loaded_selector="div#page")
        if not soup:
            logger.error("Failed to load book detail page")
            return {}

        download_page_element = soup.find("div", class_="vk-att-item")
        if not download_page_element or not download_page_element.find("a"):
            logger.error(f"Failed to find download page link for {book_dict['title']}")
            return book_dict

        download_page_link = download_page_element.find("a")["href"]
        download_url = f"https://magazinelib.com{download_page_link}"

        soup = await self.get(download_url, loaded_selector="div.docs_panel")

        download_input = soup.find("input", {"name": "url"})
        if not download_input:
            logger.error("Failed to find download link")
            return book_dict

        download_link = download_input["value"]
        logger.info(f"Found download link: {download_link}")
        book_dict["download_link"] = download_link
        return book_dict

    async def close(self):
        """Close browser and Playwright"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Browser closed")
