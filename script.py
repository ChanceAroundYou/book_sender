import asyncio
from pathlib import Path
from typing import List

from app.config import settings

settings.POSTGRES_HOST = "192.168.1.6"
settings.REDIS_HOST = "192.168.1.6"

from app.database import (
    Book,
    BookSeries,
    Task,
    User,
    UserBook,
    UserBookStatus,
    get_denpend_db,
    series,
)
from app.distributor import create_distributor
from app.task.schedulers import (
    crawl_books_scheduler,
    distribute_books_scheduler,
    download_books_scheduler,
)
from app.task.tasks import download_book_task
from app.uploader import create_uploader
from app.utils.convert_mixin import to_dict, to_iterable


def task1():
    with get_denpend_db() as db:
        user = User.get_by_id(db, 1)
        print(user.to_dict())


def task2():
    # crawl_books_scheduler.delay(1)
    # crawl_books_scheduler.delay(2)
    # crawl_books_scheduler.delay(3)
    # crawl_books_scheduler.delay(4)
    # distribute_books_scheduler.delay()
    download_books_scheduler.delay()


def task3():
    with get_denpend_db() as db:
        task = Task.query(db, first=True)
        print(task.to_dict())


def task4():
    with get_denpend_db() as db:
        book = Book.query(db, first=True)
        print(book.to_dict())


def task5():
    with get_denpend_db() as db:
        user_book = UserBook.query(db, first=True)
        print(user_book.to_dict())


def task6():
    print(to_dict(None))
    print(to_dict({}))
    print(to_iterable(None))
    print(to_iterable(1))
    print(to_iterable([]))


def task7():
    with get_denpend_db() as db:
        user = User.query(db, first=True)
        for ub in user.user_books:
            subscription = user.get_subscription(ub.book.series)
            if not subscription:
                continue
            date = subscription["subscribe_date"]
            if ub.book.date > date:
                ub.status = UserBookStatus.DOWNLOADED
                db.commit()


def task8():
    distributor = create_distributor("smtp")
    with get_denpend_db() as db:
        user = User.query(db, first=True)
        books_to_send = []
        for ub in user.user_books:
            if ub.status != UserBookStatus.DOWNLOADED:
                continue

            book = ub.book
            if book.series == "economist":
                book_dict = book.to_dict()
                # book_dict['file_path'] = book_dict['file_path'].replace('7z', 'pdf')
                # book_dict['file_format'] = 'pdf'
                books_to_send.append(book_dict)

                if len(books_to_send) >= 3:
                    break

        if books_to_send:
            asyncio.run(
                distributor.send_books(books_to_send, "chenranlin.17@gmail.com")
            )


def task9():
    file_path = "downloads/The Economist Asia Edition – 10 January 2025.pdf"
    key = file_path.split("/")[-1]
    uploader = create_uploader("r2")
    # uploader.upload_file(file_path, key)
    print(uploader.list_files())
    print(uploader.generate_presigned_url(key))


def task10():
    with get_denpend_db() as db:
        books = Book.query(db, file_format="7z")
        for book in books:
            # 构建原始7z文件路径和新的pdf文件路径
            old_path = book.file_path
            new_path = old_path.replace(".7z", ".pdf")
            if not Path(new_path).exists():
                continue

            # 更新数据库中的书籍信息
            book.update(
                file_path=new_path,
                file_format="pdf",
                file_size=Path(new_path).stat().st_size,
            )

            # 删除7z压缩包
            if Path(old_path).exists():
                Path(old_path).unlink()


def task11():
    with get_denpend_db() as db:
        books = Book.query(db)
        for book in books:
            series = BookSeries.get_series(book.title)
            book.update(series=series)


def task12():
    with get_denpend_db() as db:
        user = User.get_by_id(db, 5)
        for i in range(len(user.user_books)):
            ub: UserBook = user.user_books[i]
            if i < 2:
                ub.downloaded(force=True)
                print(ub.book.to_dict())
            else:
                break

        # for book in Book.query(db):
        #     if not book.file_path:
        #         print(book)
        #         download_book_task.delay(book.to_dict())


if __name__ == "__main__":
    # task1()
    # task2()
    # task3()
    # task4()
    # task5()
    # task6()
    # task7()
    # task8()
    # task9()
    # task10()
    # task11()
    task12()
