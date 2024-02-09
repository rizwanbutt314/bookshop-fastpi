from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from app.api import deps
from app.models import Author
from app.schemas.requests import AuthorCreateRequest
from app.schemas.responses import AuthorResponse

router = APIRouter()


@router.get("/{id}", response_model=AuthorResponse)
async def get_author(
    id: UUID4,
    session: AsyncSession = Depends(deps.get_session),
):
    """Get Author"""
    result = await session.execute(select(Author).where(Author.id == id))
    existing_author = result.scalars().first()
    if existing_author is None:
        raise HTTPException(
            status_code=404, detail="Author not found")

    return existing_author


@router.post("/", response_model=AuthorResponse)
async def create_new_author(
    new_author: AuthorCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Create new Author"""
    result = await session.execute(select(Author).where(Author.name == new_author.name and Author.birth_date == new_author.birth_date))
    if result.scalars().first() is not None:
        raise HTTPException(
            status_code=400, detail="Author with given name and birth_date already exists")
    author = Author(
        name=new_author.name,
        birth_date=new_author.birth_date,
    )
    session.add(author)
    await session.commit()
    return author
