from typing import Dict, List

import pytest

from app.task.tasks import crawl_book_task, crawl_books_task, download_book_task

BOOK_SERIES = "economist"
BOOK_DICTS: List[Dict] = [
    {
        "title": "The Economist UK – May 3, 2025",
        "date": "10.05.2025, 13:40",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/05/NtKALOcumGd3FJUFPErYUKGzx_P5NDC4nY-krSuN1nVy-5F7By_9PDr4eQQhFaPKTLgHdummKsTUbwSwVK-gEour-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-uk-may-3-2025/",
    },
    {
        "title": "The Economist Continental Europe Edition – 26 April-2 May 2025",
        "date": "09.05.2025, 15:20",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/05/BtoDkPhJ_LMBRU6-BjeH6STphYiCTwuLeymkgNRBYLro6NQO9YdaRWMyNwT9qiTQOAc_ed3n3HEXaUi92sISdc83-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-continental-europe-edition-26-april-2-may-2025/",
    },
    {
        "title": "The Economist USA – May 3, 2025",
        "date": "08.05.2025, 00:20",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/05/3CjNpE8BrRGQKryVrnDFVqjIa44Hj5PwdetYcCuiKeVSbRq7oplJX-Jq52hx-GODa1LaHZEqywiOZwVdslVXVSr-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-usa-may-3-2025/",
    },
    {
        "title": "The Economist USA – 26 April 2025",
        "date": "02.05.2025, 23:20",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/QVXnvJAU-fk8bznFG_6ne2cpvmHrOIs3lpNfXpvY_xxuABGwvl0DPnE3Wvw5Dkogsc7IUlN7gsOc543sTVfH-sx_-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-usa-26-april-2025/",
    },
    {
        "title": "The Economist UK – 26 April 2025",
        "date": "02.05.2025, 08:40",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/yCQqDHlkomNof0n7H6jD_ka_FUC3AS2dSn1IdRN5-M-7jaP3hXRSeH9AteHBXKDHy4QEPgsGUK7witM8nbo7MDsL-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-uk-26-april-2025/",
    },
    {
        "title": "The Economist Continental Europe Edition – 19-25 April 2025",
        "date": "30.04.2025, 09:20",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/PWlgoh8zfeTWk-XXOv5oZjfxfSLhWVozdb447hqWzqgetCG2QIAMpncm2g3HJ0RN-aKNXv4GndHPNr8731aildiQ-332x444.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-continental-europe-edition-19-25-april-2025/",
    },
    {
        "title": "The Economist USA – April 19, 2025",
        "date": "27.04.2025, 23:40",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/JSghbNtv8-l4E0MlTUqLp7XtupgMASTTMlh1bE4K4EeRTD9iSS9ZBE-MIpQtI7Fsdyx5zC_Vc5hMgwNYqEBm0Xqo-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-usa-april-19-2025/",
    },
    {
        "title": "The Economist UK – 19 April 2025",
        "date": "27.04.2025, 19:20",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/wOb9_K1GPOuTBZEFnL-mtnNzYSB6tm8g2B8tZYwNf1f42ouE7VeL32zER30VYnpDaSjNwYAJAVI3KF5QSklCrUae-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-uk-19-april-2025/",
    },
    {
        "title": "The Economist Continental Europe Edition – 12-19 April 2025",
        "date": "23.04.2025, 16:20",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/o6CaryqWSMoFA3wwtJq9MQjBWe9QHX1zTf3J1AZypMmsgKIvPgmioJ-w9Cfe4NxfPm_MLEhE6ilPH9eZzdNqtCgM-332x445.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-continental-europe-edition-12-19-april-2025/",
    },
    {
        "title": "The Economist USA – 12 April 2025",
        "date": "20.04.2025, 14:20",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/dmkPtDLyshqHXN-1mDfZ8FLEaDAPP8qIG7t0yeAGuZQfpI9U-G3aC0f0zRSEaWH7HzcKlrMYyrrhjrcYrQQFA3AW-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-usa-12-april-2025/",
    },
    {
        "title": "The Economist UK – 12 April 2025",
        "date": "20.04.2025, 06:00",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/X3xgsktkZhsexG3coP7fJbQgFlpbpuz9f0VGjzBEavYzX5ltryXXPS4ZC0J5CEY6ITBIoemXvbEm9mtVhGd7Y6iX-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-uk-12-april-2025/",
    },
    {
        "title": "The Economist Continental Europe Edition – 5-11 April 2025",
        "date": "16.04.2025, 12:40",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/R0QqCChiPbtAw-kFW5V8Lg1FJUFZQsJEKiS_zpi8c8KXHmE8KozH_f7b0ImGLCd4IUYXH5w8I8Es5n2xiS5aTcWI-332x445.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-continental-europe-edition-5-11-april-2025/",
    },
    {
        "title": "The Economist UK – 5 April 2025",
        "date": "13.04.2025, 12:00",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/S47luev99vcRsPg6OXILE7g4dq3VpJxc332zcMCcHO_zDArmMBRcbvNO_FWpt4ZH6-a7dV_KuwnZ1wX5FeRxX78G-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-uk-5-april-2025/",
    },
    {
        "title": "The Economist USA – April 5, 2025",
        "date": "10.04.2025, 23:40",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/7lykzAodvvuUiFiQdoXO6kL2Y04VEZCWuJT_PanN81zw8b9-NUgMvVqsjyVg8o4v5dXr22SN5UHl8aU0ppLQqkW9-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-usa-april-5-2025/",
    },
    {
        "title": "The Economist Continental Europe Edition – 29 March-4 April 2025",
        "date": "08.04.2025, 15:20",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/T3LJtqaQ2NYFNBmPOAnVNF9gOFhEj2xGymQH_zPJ9TT5jH5aGuFyiXupI4z1jnkpqaXYQJhP0lMJ54Kzk8kB4xPK-332x444.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-continental-europe-edition-29-march-4-april-2025/",
    },
    {
        "title": "The Economist UK – March 29, 2025",
        "date": "04.04.2025, 06:20",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/04/FeHvCjxnZy7WwMcbUngjx-3a4Jo7TFIOQ-hUUJ512WGSYgtptt-BTkzojvplwbzyaxWV3nSZMbtXV8HiWugp9b1c-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-uk-march-29-2025/",
    },
    {
        "title": "The Economist USA – March 29, 2025",
        "date": "02.04.2025, 12:00",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/03/EhbH4Tt5EeU6LE3j8HJDxiDagDIR0ctLhVsVZOzAHkvryo5Gny0wB1lLj-mKm8sSKmTC9htigf1fxtJs-NXaV8w-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-usa-march-29-2025/",
    },
    {
        "title": "The Economist Continental Europe Edition – 28 March 2025",
        "date": "28.03.2025, 08:40",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/03/5D_k57Mnbl439i5oMHGPb_Xhc8HnUmR7YCE2BgfqMCU_uTQe-5HPJezji2jt78yk9bLN2TKltvVo6OfbsEiXOt1o-332x445.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-continental-europe-edition-28-march-2025/",
    },
    {
        "title": "The Economist USA – 22 March 2025",
        "date": "27.03.2025, 13:45",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/03/IAJE3jpmNCVn2FjheGRkmZhbyfHDaLglwMgaTBYE6k9uEku_TM5OHeTms8B3Y5zi7qsYpj3BmWo0F_xLBO1hGgc3-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-usa-22-march-2025/",
    },
    {
        "title": "The Economist UK – 22 March 2025",
        "date": "26.03.2025, 01:40",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/03/NXsIOdC00vbDhwJlxiHS0vwrWU4rHgdtdN8gH6E07yavbTFGChfXits4N8181d7zbWnC2LhB8KZb4xODUWDFP340-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-uk-22-march-2025/",
    },
    {
        "title": "The Economist USA – 15 March 2025",
        "date": "21.03.2025, 18:15",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/03/126_C_Gh-oa5Si_QJXPMFL0PecclLIE-faK1fJTH_OOp6ugXosmY8JIRZG0vz-APtiHXwu5PYYA7vZ1tvXIQHQuG-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-usa-15-march-2025/",
    },
    {
        "title": "The Economist UK – 15 March 2025",
        "date": "20.03.2025, 10:40",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/03/ulOwkP9fkoF83zj8nerQIzn5yt656KzHcM-aCDfseSnm-1XlK9M4-vN338YeRL4B9szTheEV6YkiS3RLc41aTXD_-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-uk-15-march-2025/",
    },
    {
        "title": "The Economist Continental Europe Edition – 21 March 2025",
        "date": "19.03.2025, 07:00",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/03/psSZFK2SHC-VJq8YGbppZMCPEU0-w3Ogz7wP_FuXHZq-fDiXt0FUP0RNcGmh4RsbPgZBB1v1IfBdgkPCKiNBhuIm-332x445.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-continental-europe-edition-21-march-2025/",
    },
    {
        "title": "The Economist Continental Europe Edition – 14 March 2025",
        "date": "16.03.2025, 12:00",
        "author": "",
        "summary": "",
        "cover_link": "https://magazinelib.com/wp-content/uploads/2025/03/amrCzu43rxUgY43zRWZLfO9Hix5xFr2_JN9LOVGr_JRisxsY-FyhJ5i9l-CADVWGY34yAatk039n22xOb-NlGN9e-332x443.jpg",
        "download_link": "",
        "file_path": "",
        "file_format": "",
        "file_size": None,
        "downloaded_at": None,
        "detail_link": "https://magazinelib.com/all/the-economist-continental-europe-edition-14-march-2025/",
    },
]
BOOK_DICT: Dict = {
    "title": "The Economist UK – May 3, 2025",
    "date": "10.05.2025, 13:40",
    "author": "",
    "summary": "",
    "cover_link": "https://magazinelib.com/wp-content/uploads/2025/05/NtKALOcumGd3FJUFPErYUKGzx_P5NDC4nY-krSuN1nVy-5F7By_9PDr4eQQhFaPKTLgHdummKsTUbwSwVK-gEour-332x443.jpg",
    "download_link": "https://psv4.userapi.com/s/v1/d/RyFRN1PhXFKZUWnc9_tY70I8k1cpJiWxlY6tRf7eB5i09AGPMJoB7jEFDSwn8afAB7sx77Rnfm5TbXDda10Z2aJ4rgtGK3FJ0GzpXEMTMFXLkSWo/The_Economist_UK_-_May_3_2025.pdf",
    "file_path": "",
    "file_format": "",
    "file_size": None,
    "downloaded_at": None,
    "detail_link": "https://magazinelib.com/all/the-economist-uk-may-3-2025/",
}
DOWNLOAD_BOOK_DICT: Dict = {
    "title": "The Economist UK – May 3, 2025",
    "date": "10.05.2025, 13:40",
    "author": "",
    "summary": "",
    "cover_link": "https://magazinelib.com/wp-content/uploads/2025/05/NtKALOcumGd3FJUFPErYUKGzx_P5NDC4nY-krSuN1nVy-5F7By_9PDr4eQQhFaPKTLgHdummKsTUbwSwVK-gEour-332x443.jpg",
    "download_link": "https://psv4.userapi.com/s/v1/d/RyFRN1PhXFKZUWnc9_tY70I8k1cpJiWxlY6tRf7eB5i09AGPMJoB7jEFDSwn8afAB7sx77Rnfm5TbXDda10Z2aJ4rgtGK3FJ0GzpXEMTMFXLkSWo/The_Economist_UK_-_May_3_2025.pdf",
    "file_path": "downloads/The Economist UK – May 3, 2025.pdf",
    "file_format": "pdf",
    "file_size": 69472500,
    "downloaded_at": 0,
    "detail_link": "https://magazinelib.com/all/the-economist-uk-may-3-2025/",
}


@pytest.mark.asyncio
async def test_crawl_book_list():
    """测试爬取书籍列表任务"""
    # 执行任务
    result = crawl_books_task.delay(series=BOOK_SERIES, page=1).get()

    # 验证结果
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "result" in result, "Result should contain 'result' key"

    book_dicts = result["result"]
    assert isinstance(book_dicts, list), "Book dicts should be a list"
    assert len(book_dicts) > 0, "Should return at least one book"

    # 验证前5本书的数据
    for i in range(min(len(book_dicts), 5)):
        book_dict = book_dicts[i]
        expected_book = BOOK_DICTS[i]

        assert isinstance(book_dict, dict), f"Book {i} should be a dictionary"
        assert all(key in book_dict for key in ["title", "date", "detail_link"]), (
            f"Book {i} should contain required fields"
        )

        assert book_dict["title"] == expected_book["title"], f"Book {i} title mismatch"
        assert book_dict["date"] == expected_book["date"], f"Book {i} date mismatch"
        assert book_dict["detail_link"] == expected_book["detail_link"], (
            f"Book {i} detail_link mismatch"
        )


@pytest.mark.asyncio
async def test_crawl_book():
    """测试爬取单本书籍任务"""
    result = crawl_book_task.delay(series=BOOK_CATEGORY, book_dict=BOOK_DICTS[0]).get()

    # 验证结果
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "result" in result, "Result should contain 'result' key"

    book_dict = result["result"]
    assert isinstance(book_dict, dict), "Book dict should be a dictionary"
    assert "download_link" in book_dict, "Book dict should contain download_link"
    assert book_dict["download_link"], "Download link should not be empty"


@pytest.mark.asyncio
async def test_download_book():
    """测试下载书籍任务"""
    result = download_book_task.delay(book_dict=BOOK_DICT).get()

    # 验证结果
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "result" in result, "Result should contain 'result' key"

    download_book_dict = result["result"]
    assert isinstance(download_book_dict, dict), (
        "Download book dict should be a dictionary"
    )

    # 验证必要字段
    required_fields = ["file_path", "file_format", "file_size", "downloaded_at"]
    assert all(field in download_book_dict for field in required_fields), (
        "Download book dict should contain all required fields"
    )

    # 验证字段值
    assert download_book_dict["file_path"] == DOWNLOAD_BOOK_DICT["file_path"], (
        "File path mismatch"
    )
    assert download_book_dict["file_format"] == DOWNLOAD_BOOK_DICT["file_format"], (
        "File format mismatch"
    )
    assert download_book_dict["file_size"] == DOWNLOAD_BOOK_DICT["file_size"], (
        "File size mismatch"
    )
    assert download_book_dict["downloaded_at"] != 0, (
        "Download timestamp should not be 0"
    )
