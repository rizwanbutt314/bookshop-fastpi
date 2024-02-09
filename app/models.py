"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
import uuid

import datetime

from sqlalchemy.sql import func
from sqlalchemy import String, DateTime, Date, Integer, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Author(Base):
    __tablename__ = "author"

    name: Mapped[str] = mapped_column(
        String(254), nullable=False, index=True
    )
    birth_date: Mapped[datetime.date] = mapped_column(
        Date(), nullable=False
    )
    books = relationship('Book', back_populates='author')


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(
        String(254), nullable=False, index=True
    )
    publishing_year: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    barcode: Mapped[str] = mapped_column(
        String(254), nullable=False, index=True
    )
    author_id = Column(UUID, ForeignKey('author.id'))
    author = relationship('Author', back_populates='books')

    stores = relationship('Store', back_populates='book')


class Store(Base):
    __tablename__ = "stores"

    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    date: Mapped[datetime.date] = mapped_column(
        Date(), nullable=False
    )

    book_id = Column(UUID, ForeignKey('books.id'))
    book = relationship('Book', back_populates='stores')