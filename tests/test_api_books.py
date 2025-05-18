import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.core import get_db
from app.database.base import BaseModel
from app.database.book import Book
from app.main import app

# 测试数据
TEST_BOOK = {
    "title": "Test Book",
    "author": "Test Author",
    "date": "2025-05-12",
    "summary": "Test Summary",
    "cover_link": "http://example.com/cover.jpg",
    "download_link": "http://example.com/book.pdf",
    "category": "Test Category",
    "file_format": "pdf",
}


# 设置测试数据库
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    BaseModel.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session")
def client(db_engine):
    TestingSessionLocal = sessionmaker(bind=db_engine)

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


# 创建测试图书
@pytest.fixture(scope="function")
def test_book(db_session):
    book = Book(**TEST_BOOK)
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book


# 测试用例
def test_get_books(client):
    """测试获取图书列表"""
    response = client.get("/api/v1/books")  # 注意：确保路径与你的API路由匹配
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_book(client, test_book):
    """测试获取单本图书"""
    response = client.get(f"/api/v1/books/{test_book.id}")
    assert response.status_code == 200
    assert response.json()["title"] == TEST_BOOK["title"]


def test_get_nonexistent_book(client):
    """测试获取不存在的图书"""
    response = client.get("/api/v1/books/999")
    assert response.status_code == 404


def test_create_book(client):
    """测试创建图书"""
    response = client.post("/api/v1/books", json=TEST_BOOK)
    assert response.status_code == 200
    assert response.json()["title"] == TEST_BOOK["title"]


def test_update_book(client, test_book):
    """测试更新图书"""
    update_data = {"title": "Updated Title"}
    response = client.put(f"/api/v1/books/{test_book.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_update_nonexistent_book(client):
    """测试更新不存在的图书"""
    response = client.put("/api/v1/books/999", json={"title": "Updated Title"})
    assert response.status_code == 404


def test_delete_book(client, test_book):
    """测试删除图书"""
    response = client.delete(f"/api/v1/books/{test_book.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"


def test_delete_nonexistent_book(client):
    """测试删除不存在的图书"""
    response = client.delete("/api/v1/books/999")
    assert response.status_code == 404
