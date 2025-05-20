import os
from datetime import datetime

import pytest

from app.distributor import create_distributor, SMTPDistributor
from app.task.tasks import distribute_book_task

TEST_FILES_DIR = "tests/test_files"
TEST_PDF_PATH = os.path.join(TEST_FILES_DIR,"test.pdf")

@pytest.fixture(scope="module")
def test_files():
    """创建测试文件夹和PDF文件的fixture"""
    # 设置：创建测试文件
    os.makedirs(TEST_FILES_DIR, exist_ok=True)
    with open(TEST_PDF_PATH, "wb") as f:
        f.write(b"Test PDF content" * 1000)  # 创建一个假的PDF文件
    
    yield  # 运行测试
    
    # 清理：删除测试文件
    if os.path.exists(TEST_PDF_PATH):
        os.remove(TEST_PDF_PATH)
    if os.path.exists(TEST_FILES_DIR):
        os.rmdir(TEST_FILES_DIR)

@pytest.fixture
def test_email() -> str:
    """测试邮箱"""
    return "chenranlin.17@gmail.com"

@pytest.fixture
def test_book():
    """创建测试用书籍对象的fixture"""
    return {
        "title": "Test Book",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "file_path": TEST_PDF_PATH,
        "file_size": 1024 * 1024,  # 1MB
        "download_link": "https://example.com/test.pdf",
    }

@pytest.fixture
def distributor() -> SMTPDistributor:
    """创建邮件分发器实例的fixture"""
    return create_distributor('smtp')

@pytest.mark.asyncio
async def test_single_book_distribution(test_files, test_book, distributor, test_email):
    """测试单本书籍发送"""
    success = await distributor.send_book(test_book, email=test_email)
    assert success, "单本书籍发送失败"

@pytest.mark.asyncio
async def test_batch_books_distribution(test_files, test_book, distributor, test_email):
    """测试批量书籍发送"""
    books = [test_book, test_book]  # 使用同一本书测试批量发送
    success = await distributor.send_books(books, email=test_email)
    assert success, "批量书籍发送失败"

@pytest.mark.asyncio
async def test_distribution_with_invalid_file(distributor, test_email):
    """测试发送不存在的文件"""
    invalid_book = {
        "title": "Invalid Book",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "file_path": "non_existent.pdf",
        "file_size": 1024,
        "download_link": "https://example.com/invalid.pdf"
    }
    
    with pytest.raises(Exception) as exc_info:
        await distributor.send_book(invalid_book, email=test_email)
    assert "文件未找到" in str(exc_info.value)

@pytest.mark.asyncio
async def test_distribution_with_custom_recipient(test_files, test_book, distributor, test_email):
    """测试发送到自定义收件人"""
    custom_recipient = "test@example.com"
    success = await distributor.send_book(test_book, email=test_email)
    assert success, f"发送到自定义收件人 {custom_recipient} 失败" 

@pytest.mark.asyncio
async def test_celery_book_distribution_task(test_files, test_book, test_email):
    """测试Celery异步发送书籍任务"""
    # 执行异步任务
    book_dict = test_book
    print(book_dict)
    result = distribute_book_task.delay(
        book_dict=book_dict,
        email=test_email
    )
    
    # 等待任务完成并获取结果
    task_result = result.get()  # 30秒超时
    assert task_result is not False, "Celery任务执行失败"
