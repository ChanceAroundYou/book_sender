from datetime import datetime

import pytest

from app.uploader import create_uploader


@pytest.fixture
def test_file(tmp_path):
    """创建测试文件"""
    file_path = tmp_path / "test.txt"
    content = "This is a test file"
    file_path.write_text(content)
    return str(file_path)


@pytest.fixture
def s3_uploader():
    """创建 S3 上传器"""
    return create_uploader("s3")


@pytest.fixture
def r2_uploader():
    """创建 R2 上传器"""
    return create_uploader("r2")


def test_upload_file_s3(s3_uploader, test_file):
    """测试 S3 上传文件"""
    # 上传文件
    key = s3_uploader.upload_file(test_file)
    assert key == "test.txt"

    # 检查文件是否存在
    assert s3_uploader.file_exists(key)

    # 获取文件信息
    info = s3_uploader.get_file_info(key)
    assert info["key"] == key
    assert info["size"] == len("This is a test file")
    assert isinstance(info["last_modified"], datetime)

    # 生成预签名URL
    url = s3_uploader.generate_url(key)
    assert url.startswith("https://")
    assert key in url

    # 删除文件
    assert s3_uploader.delete_file(key)
    assert not s3_uploader.file_exists(key)


def test_upload_file_r2(r2_uploader, test_file):
    """测试 R2 上传文件"""
    # 上传文件
    key = r2_uploader.upload_file(test_file)
    assert key == "test.txt"

    # 检查文件是否存在
    assert r2_uploader.file_exists(key)

    # 获取文件信息
    info = r2_uploader.get_file_info(key)
    assert info["key"] == key
    assert info["size"] == len("This is a test file")
    assert isinstance(info["last_modified"], datetime)

    # 生成预签名URL
    url = r2_uploader.generate_url(key)
    assert url.startswith("https://")
    assert key in url

    # 删除文件
    assert r2_uploader.delete_file(key)
    assert not r2_uploader.file_exists(key)


def test_list_files_s3(s3_uploader, test_file):
    """测试 S3 列出文件"""
    # 上传多个文件
    keys = []
    for i in range(3):
        key = f"test_{i}.txt"
        s3_uploader.upload_file(test_file, key)
        keys.append(key)

    try:
        # 列出所有文件
        files = s3_uploader.list_files()
        assert len(files) >= 3

        # 列出特定前缀的文件
        files = s3_uploader.list_files(prefix="test_")
        assert len(files) == 3

        # 检查文件信息
        for file in files:
            assert file["key"] in keys
            assert file["size"] == len("This is a test file")
            assert isinstance(file["last_modified"], datetime)
    finally:
        # 清理文件
        s3_uploader.delete_files(keys)


def test_list_files_r2(r2_uploader, test_file):
    """测试 R2 列出文件"""
    # 上传多个文件
    keys = []
    for i in range(3):
        key = f"test_{i}.txt"
        r2_uploader.upload_file(test_file, key)
        keys.append(key)

    try:
        # 列出所有文件
        files = r2_uploader.list_files()
        assert len(files) >= 3

        # 列出特定前缀的文件
        files = r2_uploader.list_files(prefix="test_")
        assert len(files) == 3

        # 检查文件信息
        for file in files:
            assert file["key"] in keys
            assert file["size"] == len("This is a test file")
            assert isinstance(file["last_modified"], datetime)
    finally:
        # 清理文件
        r2_uploader.delete_files(keys)


def test_delete_files_s3(s3_uploader, test_file):
    """测试 S3 批量删除文件"""
    # 上传多个文件
    keys = []
    for i in range(3):
        key = f"test_{i}.txt"
        s3_uploader.upload_file(test_file, key)
        keys.append(key)

    try:
        # 批量删除文件
        results = s3_uploader.delete_files(keys)
        assert len(results) == 3
        assert all(results.values())

        # 确认文件已删除
        for key in keys:
            assert not s3_uploader.file_exists(key)
    finally:
        # 确保清理
        s3_uploader.delete_files(keys)


def test_delete_files_r2(r2_uploader, test_file):
    """测试 R2 批量删除文件"""
    # 上传多个文件
    keys = []
    for i in range(3):
        key = f"test_{i}.txt"
        r2_uploader.upload_file(test_file, key)
        keys.append(key)

    try:
        # 批量删除文件
        results = r2_uploader.delete_files(keys)
        assert len(results) == 3
        assert all(results.values())

        # 确认文件已删除
        for key in keys:
            assert not r2_uploader.file_exists(key)
    finally:
        # 确保清理
        r2_uploader.delete_files(keys)


def test_file_not_found_s3(s3_uploader):
    """测试 S3 文件不存在的情况"""
    key = "non_existent.txt"

    # 检查文件是否存在
    assert not s3_uploader.file_exists(key)

    # 获取文件信息应该抛出异常
    with pytest.raises(FileNotFoundError):
        s3_uploader.get_file_info(key)

    # 删除不存在的文件应该返回 False
    assert not s3_uploader.delete_file(key)


def test_file_not_found_r2(r2_uploader):
    """测试 R2 文件不存在的情况"""
    key = "non_existent.txt"

    # 检查文件是否存在
    assert not r2_uploader.file_exists(key)

    # 获取文件信息应该抛出异常
    with pytest.raises(FileNotFoundError):
        r2_uploader.get_file_info(key)

    # 删除不存在的文件应该返回 False
    assert not r2_uploader.delete_file(key)


def test_upload_and_get_url_s3(s3_uploader, test_file):
    """测试 S3 上传并获取URL"""
    # 上传文件并获取URL
    url = s3_uploader.upload_and_get_url(test_file)
    assert url.startswith("https://")
    assert "test.txt" in url

    # 清理文件
    s3_uploader.delete_file("test.txt")


def test_upload_and_get_url_r2(r2_uploader, test_file):
    """测试 R2 上传并获取URL"""
    # 上传文件并获取URL
    url = r2_uploader.upload_and_get_url(test_file)
    assert url.startswith("https://")
    assert "test.txt" in url

    # 清理文件
    r2_uploader.delete_file("test.txt")
