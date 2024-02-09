import uuid

from httpx import AsyncClient, codes
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from app.main import app
from app.models import Author, Book, Store


async def test_add_new_book(
    client: AsyncClient, session: AsyncSession
):
    
    # add test data
    test_author = Author(name="TA 1", birth_date=datetime.date.today())
    session.add(test_author)
    await session.commit()

    # with valid data
    response = await client.post(
        app.url_path_for("create_new_book"),
        json={
            "title": "Test Book 1",
            "barcode": "tb1",
            "publishing_year": 2020,
            "author": test_author.id
        },
    )
    assert response.status_code == codes.OK
    result = await session.execute(select(Book).where(Book.barcode == "tb1"))
    book = result.scalars().first()
    assert book is not None

    # without title of book
    response = await client.post(
        app.url_path_for("create_new_book"),
        json={
            "barcode": "tb1",
            "publishing_year": 2020,
            "author": test_author.id
        },
    )
    assert response.status_code == 422 # missing schema

    # publishing year less than 1900
    response = await client.post(
        app.url_path_for("create_new_book"),
        json={
            "title": "Test Book 1",
            "barcode": "tb1",
            "publishing_year": 1800,
            "author": test_author.id
        },
    )
    assert response.status_code == 422 # missing schema


async def test_get_books(
    client: AsyncClient, session: AsyncSession
):
    # ------ test data
    test_author_1 = Author(name="TA 1", birth_date=datetime.date.today())
    test_author_2 = Author(name="TA 2", birth_date=datetime.date.today())
    session.add(test_author_1)
    await session.commit()
    session.add(test_author_2)
    await session.commit()

    # # books data
    test_book_1 = Book(title="TB 1", barcode="tb1",
                        publishing_year=2005, author_id=uuid.UUID(test_author_1.id))
    test_book_2 = Book(title="TB 2", barcode="tb2",
                        publishing_year=2006, author_id=uuid.UUID(test_author_1.id))
    test_book_3 = Book(title="TB 3", barcode="ta3-tb2",
                        publishing_year=1980, author_id=uuid.UUID(test_author_2.id))
    session.add(test_book_1)
    await session.commit()
    session.add(test_book_2)
    await session.commit()
    session.add(test_book_3)
    await session.commit()

    # store data
    book_1_store_1 = Store(quantity=5, date=datetime.datetime(2024, 2, 1), book_id=uuid.UUID(test_book_1.id))
    book_1_store_2 = Store(quantity=3, date=datetime.datetime(2024, 2, 5), book_id=uuid.UUID(test_book_1.id))
    book_1_store_3 = Store(quantity=-2, date=datetime.datetime(2024, 2, 9), book_id=uuid.UUID(test_book_1.id))
    session.add(book_1_store_1)
    await session.commit()
    session.add(book_1_store_2)
    await session.commit()
    session.add(book_1_store_3)
    await session.commit()

    book_2_store_1 = Store(quantity=8, date=datetime.datetime(2024, 2, 5), book_id=uuid.UUID(test_book_2.id))
    book_2_store_2 = Store(quantity=-5, date=datetime.datetime(2024, 2, 9), book_id=uuid.UUID(test_book_2.id))
    session.add(book_2_store_1)
    await session.commit()
    session.add(book_2_store_2)
    await session.commit()

    book_3_store_1 = Store(quantity=7, date=datetime.datetime(2024, 2, 9), book_id=uuid.UUID(test_book_3.id))
    session.add(book_3_store_1)
    await session.commit()

    # ------ test data

    # get all books
    response = await client.get(f"/book/")
    data = response.json()
    assert response.status_code == 200
    assert data["found"] == 3

    # search books using barcode
    response = await client.get(f"/book/?barcode=tb")
    data = response.json()
    assert response.status_code == 200
    assert data["found"] == 2

    response = await client.get(f"/book/?barcode=ta3")
    data = response.json()
    assert response.status_code == 200
    assert data["found"] == 1


    # ---- History

    # get all books hisotry
    response = await client.get(f"/history/")
    history_data = response.json()
    assert response.status_code == 200

    for history in history_data:
        assert history["book"]["title"] in ["TB 1", "TB 2", "TB 3"]
        assert history["start_balance"] in [6, 3, 7]


    response = await client.get(f"/history/?barcode=tb1")
    history_data = response.json()
    assert response.status_code == 200

    for history in history_data:
        assert history["book"]["title"] in ["TB 1"]
        assert history["start_balance"] in [6]

    response = await client.get(f"/history/?start=2024-02-05&end=2024-02-09")
    history_data = response.json()
    assert response.status_code == 200

    assert history_data[0]['start_balance'] == 8
    assert history_data[0]['end_balance'] == 6
    assert history_data[1]['start_balance'] == 8
    assert history_data[1]['end_balance'] == 3
    assert history_data[2]['start_balance'] == None
    assert history_data[2]['end_balance'] == 7