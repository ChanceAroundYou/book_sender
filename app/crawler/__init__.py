"""
Crawler module for The Economist Magazine
"""

from app.crawler.economist_crawler import EconomistCrawler
from app.crawler.base import BaseCrawler
from app.crawler.factory import create_crawler

__all__ = ["EconomistCrawler", "BaseCrawler", "create_crawler"]
