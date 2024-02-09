from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy import select, func, cast, String, case
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.api import deps
from app.models import Book, Store

router = APIRouter()


@router.get("/")
async def search_history(
    start: Optional[date] = None,
    end: Optional[date] = None,
    barcode: Optional[str] = None,
    session: AsyncSession = Depends(deps.get_session),
):
    if not start:
        start = date.today()

    if not end:
        end = date.today()

    """Get History"""
    store_subquery = (
        select(
            Store.book_id,
            func.string_agg(cast(Store.quantity, String), ',').label("quantities"),
            func.string_agg(cast(Store.date, String), ',').label("dates"),
            func.sum(func.nullif(
                case((Store.date <= start, Store.quantity), else_=0),
                0
            )).label("start_balance"),
            func.sum(func.nullif(
                case((Store.date <= end, Store.quantity), else_=0),
                0
            )).label("end_balance"),
        ).group_by(
            Store.book_id
        )
    ).alias("store_records")

    books_query = (
        select(
            Book.id,
            Book.title,
            Book.barcode,
            store_subquery.c.quantities,
            store_subquery.c.dates,
            store_subquery.c.start_balance,
            store_subquery.c.end_balance,
        ).join(
            store_subquery,
            Book.id == store_subquery.c.book_id
        ).order_by(
            Book.title
        )
    )
    if barcode:
        books_query = books_query.filter(Book.barcode == barcode)

    result = await session.execute(books_query, {"start": start, "end": end})
    books_data = result.fetchall()

    # Post-process the data to parse store records
    parsed_books_with_store_records = []
    for book_record in books_data:
        id, title, barcode, quantities_str, dates_str, start_balance, end_balance = book_record
        quantities = list(map(int, quantities_str.split(',')))
        dates = dates_str.split(',')
        store_records = [{"quantity": q, "date": d}
                         for q, d in zip(quantities, dates)]
        parsed_books_with_store_records.append({
            "book": {"id": id, "title": title, "barcode": barcode},
            "start_balance": start_balance,
            "end_balance": end_balance,
            "history": store_records
        })

    return parsed_books_with_store_records
