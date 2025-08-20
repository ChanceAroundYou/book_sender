import tempfile
from pathlib import Path

import pytest

from app.utils.image_downloader import ImageDownloader


@pytest.fixture
def temp_static_dir():
    """创建临时静态目录"""
    with tempfile.TemporaryDirectory() as temp_dir:
        static_dir = Path(temp_dir) / "static" / "images"
        static_dir.mkdir(parents=True, exist_ok=True)
        yield static_dir


@pytest.fixture
def image_downloader(temp_static_dir):
    """创建图片下载器实例"""
    return ImageDownloader(static_dir=temp_static_dir)


def test_get_file_extension_from_url():
    """测试从URL获取文件扩展名"""
    downloader = ImageDownloader()

    # 测试各种URL格式
    assert downloader._get_file_extension("https://example.com/image.jpg") == ".jpg"
    assert downloader._get_file_extension("https://example.com/image.png") == ".png"
    assert downloader._get_file_extension("https://example.com/image.jpeg") == ".jpeg"
    assert downloader._get_file_extension("https://example.com/image.gif") == ".gif"
    assert downloader._get_file_extension("https://example.com/image.webp") == ".webp"

    # 测试没有扩展名的URL
    assert downloader._get_file_extension("https://example.com/image") == ".jpg"


def test_get_file_extension_from_content_type():
    """测试从Content-Type获取文件扩展名"""
    downloader = ImageDownloader()

    # 测试各种Content-Type
    assert (
        downloader._get_file_extension("https://example.com/image", "image/jpeg")
        == ".jpg"
    )
    assert (
        downloader._get_file_extension("https://example.com/image", "image/png")
        == ".png"
    )
    assert (
        downloader._get_file_extension("https://example.com/image", "image/gif")
        == ".gif"
    )
    assert (
        downloader._get_file_extension("https://example.com/image", "image/webp")
        == ".webp"
    )
    assert (
        downloader._get_file_extension("https://example.com/image", "image/svg+xml")
        == ".svg"
    )


def test_generate_filename():
    """测试生成文件名"""
    downloader = ImageDownloader()

    title = "The Economist UK – May 3, 2025"
    url = "https://example.com/image.jpg"

    filename = downloader._generate_filename(title, url)

    # 检查文件名格式
    assert "The-Economist-UK-May-3-2025" in filename
    assert len(filename) > 20  # 应该包含哈希值


@pytest.mark.asyncio
async def test_download_image_success(image_downloader):
    """测试成功下载图片"""
    # 使用一个公开的测试图片URL
    url = "https://httpbin.org/image/png"
    title = "Test Image"

    result = await image_downloader.download_image(url, title)

    assert result is not None
    assert Path(result).exists()
    assert Path(result).suffix == ".png"


@pytest.mark.asyncio
async def test_download_image_invalid_url(image_downloader):
    """测试无效URL"""
    url = "https://invalid-url-that-does-not-exist.com/image.jpg"
    title = "Test Image"

    result = await image_downloader.download_image(url, title)

    assert result is None


@pytest.mark.asyncio
async def test_download_image_empty_url(image_downloader):
    """测试空URL"""
    url = ""
    title = "Test Image"

    result = await image_downloader.download_image(url, title)

    assert result is None


@pytest.mark.asyncio
async def test_download_image_duplicate(image_downloader):
    """测试重复下载同一图片"""
    url = "https://httpbin.org/image/png"
    title = "Test Image"

    # 第一次下载
    result1 = await image_downloader.download_image(url, title)
    assert result1 is not None

    # 第二次下载相同图片
    result2 = await image_downloader.download_image(url, title)
    assert result2 is not None

    # 应该返回相同的路径
    assert result1 == result2
