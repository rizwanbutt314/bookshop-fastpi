from httpx import AsyncClient, codes
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.main import app
from app.models import Author


async def test_add_new_author(
    client: AsyncClient, session: AsyncSession
):
    response = await client.post(
        app.url_path_for("create_new_author"),
        json={
            "name": "Test Author 1",
            "birth_date": "2023-01-01",
        },
    )
    assert response.status_code == codes.OK
    result = await session.execute(select(Author).where(Author.name == "Test Author 1"))
    auhtor = result.scalars().first()
    assert auhtor is not None

    # without name of author
    response = await client.post(
        app.url_path_for("create_new_author"),
        json={
            "birth_date": "2023-01-01",
        },
    )
    assert response.status_code == 422  # missing schema


async def test_get_author(
    client: AsyncClient, session: AsyncSession
):
    # add test author
    test_author = Author(name="TA 1", birth_date=date.today())
    session.add(test_author)
    await session.commit()

    response = await client.get(f"/author/{test_author.id}")
    assert response.status_code == codes.OK
