
import asyncio

from app.database import (get_db, User, Book, UserBook, UserBookStatus,
                          Task)
from app.distributor import create_distributor
from app.task.schedulers import (add_books_to_users, check_download,
                                 distribute_books, send_books)
from app.utils.convert_mixin import to_dict, to_iterable, to_json


def task1():
    with get_db() as db:
        user = User.get_by_id(db, 1)
        print(user.to_dict())

def task2():
    # add_books_to_users.delay()
    # check_new_books.delay()
    distribute_books.delay()


def task3():
    with get_db() as db:
        task = Task.query(db, first=True)
        print(task.to_dict())

def task4():
    with get_db() as db:
        book = Book.query(db, first=True)
        print(book.to_dict())

def task5():
    with get_db() as db:
        user_book = UserBook.query(db, first=True)
        print(user_book.to_dict())

def task6():
    print(to_dict(None))
    print(to_dict({}))
    print(to_iterable(None))
    print(to_iterable(1))
    print(to_iterable([]))

def task7():
    with get_db() as db:
        user = User.query(db, first=True)
        for ub in user.user_books:
            subscription = user.get_subscription(ub.book.category)
            if not subscription:
                continue
            date = subscription['subscribe_date']
            if ub.book.date > date:
                ub.status = UserBookStatus.DOWNLOADED
                db.commit()

def task8():
    distributor = create_distributor('ses')
    with get_db() as db:
        user = User.query(db, first=True)
        for ub in user.user_books:
            if ub.status != UserBookStatus.DOWNLOADED:
                continue

            book = ub.book
            if book.category == 'economist':
                book_dict = book.to_dict()
                # book_dict['file_path'] = book_dict['file_path'].replace('\\', '/')
                # book_dict['file_path'] = book_dict['file_path'].replace('7z', 'pdf')
                # book_dict['file_format'] = 'pdf'
                # book_dict['file_size'] = 
                asyncio.run(distributor.send_book(book_dict, 'xkb1@xiaokubao.space'))
                break

    
if __name__ == "__main__":
    # task1()
    # task2()
    # task3()
    # task4()
    # task5()
    # task6()
    # task7()
    task8()

