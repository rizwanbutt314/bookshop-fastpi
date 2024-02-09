from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from app.api import deps
from app.models import Author, Book, Store
from app.schemas.requests import BookCreateRequest
from app.schemas.responses import BookResponse, AuthorResponse

router = APIRouter()


@router.get("/{id}")
async def get_book(
    id: UUID4,
    session: AsyncSession = Depends(deps.get_session),
):
    """Get Book Data"""
    result = await session.execute(
        select(
            Book,
            Author,
            func.sum(Store.quantity)
        )
        .join(Author)
        .join(Store, Book.id == Store.book_id)
        .group_by(Book.id, Author.id)
        .options(selectinload(Book.author))
        .where(Book.id == id)
    )
    book_data = result.first()

    if book_data is None:
        raise HTTPException(
            status_code=404, detail="Book not found")

    book, author, total_quantity = book_data

    # Author object
    author_data = AuthorResponse(
        id=author.id, name=author.name, birth_date=author.birth_date)

    return BookResponse(id=book.id, title=book.title, publishing_year=book.publishing_year, barcode=book.barcode, quantity=total_quantity, author=author_data)


@router.post("/")
async def create_new_book(
    new_book: BookCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Create new Book"""
    result = await session.execute(select(Author).where(Author.id == new_book.author))
    author_db = result.scalars().first()
    if author_db is None:
        raise HTTPException(
            status_code=400, detail="Author with given id not found")

    book = Book(
        title=new_book.title,
        barcode=new_book.barcode,
        publishing_year=new_book.publishing_year,
        author=author_db,
    )
    session.add(book)
    await session.commit()
    return ""


@router.get("/")
async def search_books(
    barcode: Optional[str] = None,
    session: AsyncSession = Depends(deps.get_session),
):
    """Search Books"""
    books_query = (select(
        Book,
        Author,
        func.sum(Store.quantity)
    )
        .join(Author)
        .join(Store, Book.id == Store.book_id)
        .group_by(Book.id, Author.id)
        .options(selectinload(Book.author))
    )

    if barcode:
        books_query = books_query.filter(Book.barcode.startswith(barcode))

    result = await session.execute(books_query)
    book_data = result.fetchall()

    all_items = list()
    item_count = 0
    for book, author, total_quantity in book_data:
        author_data = AuthorResponse(
            id=author.id, name=author.name, birth_date=author.birth_date)
        book_data = BookResponse(id=book.id, title=book.title, publishing_year=book.publishing_year,
                                 barcode=book.barcode, quantity=total_quantity, author=author_data)
        all_items.append(book_data)
        item_count += 1

    return {
        'found': item_count,
        'items': all_items
    }
