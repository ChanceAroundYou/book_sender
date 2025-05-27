import os
import random
import re
import time
from datetime import datetime
from typing import List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from loguru import logger
from playwright.async_api import async_playwright

from app.crawler.base import BaseCrawler
from app.utils.image_processor import ImageProcessor


class EconomistCrawler(BaseCrawler):
    def __init__(self, base_url="https://magazinelib.com/all/the-economist/page/{}/"):
        super().__init__(base_url)
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.image_processor = ImageProcessor(debug=False)
        self.series_name = "the-economist"
        logger.info(f"Initialized crawler for series: {self.series_name}")

    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.init_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.close()

    async def init_browser(self):
        """初始化浏览器"""
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

    async def _find_and_click_checkbox(self):
        """查找并点击 checkbox"""
        screenshot_path = await self._take_screenshot()
        # 在图像中查找 checkbox
        checkbox_pos = self.image_processor.find_checkbox(screenshot_path)
        # 删除截图文件
        # if os.path.exists(screenshot_path):
        #     os.remove(screenshot_path)
            # logger.debug(f"删除截图: {screenshot_path}")

        if checkbox_pos:
            # 如果找到 checkbox，点击它
            x, y = checkbox_pos
            x += random.randint(-5, 5)
            y += random.randint(-5, 5)
            await self.page.mouse.click(x, y)
            logger.info(f"点击 ({x}, {y})")
            await self.delay(1, 3)
            return True
        else:
            # logger.info(")
            return False

    async def _take_screenshot(self, save_dir: str = "tmp"):
        """截取指定区域的屏幕截图"""
        # 创建保存目录
        os.makedirs(save_dir, exist_ok=True)
        now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        screenshot_path = os.path.join(
            save_dir, f"{now}_{random.randint(1, 50):02d}_full.png"
        )

        # 使用 Playwright 截图
        await self.page.screenshot(path=screenshot_path)
        return screenshot_path

    async def get(self, url, max_wait_time=30, loaded_selector=None, soup=True):
        """安全访问页面，处理 Cloudflare 验证等情况"""
        logger.info(f"访问页面: {url}")
        await self.page.goto(url)
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            # 检查页面标题
            try:
                if "Just a moment" in await self.page.title():
                    # await self.delay(5, 10)
                    if await self._find_and_click_checkbox():
                        await self.delay(5, 10)

                # 检查页面是否加载完成
                if loaded_selector is not None:
                    loaded_element = await self.page.query_selector(loaded_selector)
                    if loaded_element:
                        content = await self.page.content()
                        if soup:
                            return BeautifulSoup(content, "html.parser")
                        else:
                            return content
                print(await self.page.title())
            except:
                pass
            # 随机延迟后继续检测
            await self.delay(1, 2)
        # 超时抛出异常
        raise TimeoutError(f"页面加载超时 ({max_wait_time}秒)")

    async def save_cover_image(
        self, cover_url: str, book_date: str, book_title: str, series: str
    ) -> str | None:
        """Downloads an image from a URL and saves it locally."""
        image_page = None  # Initialize for graceful close in finally
        try:
            logger.info(f"Downloading cover from: {cover_url}")

            soup = await self.get(cover_url, max_wait_time=60, loaded_selector="img")
            print(soup)

            # if not response or not response.ok:
            #     logger.error(
            #         f"Failed to fetch image: {cover_url}, Status: {response.status if response else 'No response'}"
            #     )
            #     return None

            # image_bytes = await response.body()

            # parsed_url = urlparse(cover_url)
            # original_filename = os.path.basename(parsed_url.path)
            # _, ext = os.path.splitext(original_filename)
            # if not ext:
            #     content_type = response.headers.get("content-type")
            #     if content_type and "image/" in content_type:
            #         ext = "." + content_type.split("image/")[-1].split(";")[0].lower()
            #     else:
            #         ext = ".jpg"

            # sanitized_title = re.sub(
            #     r'[\\/*?:"<>|]', "", book_title
            # )  # Remove invalid filename chars
            # sanitized_title = re.sub(r"[^\w\s-]", "", sanitized_title.lower())
            # sanitized_title = re.sub(r"[-\s]+", "-", sanitized_title).strip("-_")

            # filename = f"{book_date}_{sanitized_title[:50]}{ext}"

            # base_static_path = os.path.abspath(
            #     os.path.join(os.path.dirname(__file__), "..", "..", "static", "images")
            # )
            # series_image_path = os.path.join(base_static_path, series)
            # os.makedirs(series_image_path, exist_ok=True)

            # local_file_path = os.path.join(series_image_path, filename)

            # with open(local_file_path, "wb") as f:
            #     f.write(image_bytes)

            # logger.info(f"Cover saved to: {local_file_path}")

            # relative_path_for_db = os.path.join("images", series, filename).replace(
            #     "\\\\", "/"
            # )
            # return relative_path_for_db

        except Exception as e:
            logger.error(f"Error saving cover image from {cover_url}: {e}")
            return None
        finally:
            if image_page and not image_page.is_closed():
                await image_page.close()

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
            raw_cover_link = (
                cover_element["data-src"]
                if cover_element and "data-src" in cover_element.attrs
                else None
            )

            book_dict = {
                "title": title,
                "date": date,
                "series": self.series_name,
                "detail_link": detail_link,
                "cover_link": None,  # Default to None, will be populated if successfully saved
            }

            if (
                raw_cover_link and date and title
            ):  # title & date for filename, raw_cover_link for source
                local_uri = await self.save_cover_image(
                    cover_url=raw_cover_link,
                    book_date=date,
                    book_title=title,
                    series=self.series_name,
                )
                if local_uri:
                    book_dict["cover_link"] = local_uri

            book_dicts.append(book_dict)
        logger.info(f"找到 {len(book_dicts)} 期杂志")
        return book_dicts

    async def get_book(self, book_dict: dict) -> dict:
        logger.info(f"正在获取书籍详情: {book_dict['title']}")
        soup = await self.get(book_dict["detail_link"], loaded_selector="div#page")

        download_page_element = soup.find("div", class_="vk-att-item")
        download_page_link = download_page_element.find("a")["href"]
        download_url = f"https://magazinelib.com{download_page_link}"

        soup = await self.get(download_url, loaded_selector="div.docs_panel")

        download_input = soup.find("input", {"name": "url"})
        if not download_input:
            logger.error("未找到下载链接")
            return book_dict

        download_link = download_input["value"]
        logger.info(f"找到下载链接: {download_link}")
        book_dict["download_link"] = download_link
        return book_dict

    async def close(self):
        """关闭浏览器和 Playwright"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("关闭浏览器")
