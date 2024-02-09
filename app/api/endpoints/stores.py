import uuid
import pandas as pd

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.api import deps
from app.models import Store, Book
from app.schemas.requests import StoreCreateRequest

router = APIRouter()


async def add_store_quantity_for_book(session, new_store, add=True):
    result = await session.execute(select(Book).where(Book.barcode == new_store.barcode))
    book_db = result.scalars().first()
    if book_db is None:
        raise HTTPException(
            status_code=400, detail="Book with given barcode not found")

    quantity = new_store.quantity if add else -new_store.quantity
    store = Store(
        book=book_db,
        quantity=quantity,
        date=date.today(),
    )
    session.add(store)
    await session.commit()


async def process_excel_data(session, file):
    # Read the Excel file
    df = pd.read_excel(file.file, header=None, names=["barcode", "quantity"])

    df = df.astype({'barcode': 'string'})

    # quantity data validations
    try:
        first_row_with_quantity_invalid = df[df["quantity"].str.isdigit() == False].index.tolist()[
            0] + 1
        # get row data
        invalid_row_data = df.iloc[[
            first_row_with_quantity_invalid-1]].to_dict("records")
        raise HTTPException(status_code=400, detail=f"Invalid quantity value at row {first_row_with_quantity_invalid} with data: {invalid_row_data[0]}")
    except (IndexError, AttributeError):
        pass

    # barcode db validations
    df["barcode"] = df["barcode"].replace(',', '', regex=True)
    file_barcodes = df['barcode'].tolist()

    # check data in db using barcodes
    db_books = await session.execute(select(Book.id, Book.barcode).filter(Book.barcode.in_(file_barcodes)))
    db_books = db_books.fetchall()
    db_books_barcodes = {db_book[1]: db_book[0] for db_book in db_books}
    db_barcodes = set(db_books_barcodes.keys())

    # check for non-existant barcode
    missing_barcode_index = None
    missing_barcode = False
    for index, file_barcode in enumerate(file_barcodes):
        if file_barcode not in db_barcodes:
            missing_barcode_index = index + 1
            missing_barcode = True
            break

    if missing_barcode:
        raise HTTPException(status_code=400, detail=f"Invalid barcode value at row {missing_barcode_index}")

    # Ingest data into the database
    for index, row in df.iterrows():
        if not row["barcode"]:
            continue

        book_id = db_books_barcodes[row["barcode"]]
        store_entry = Store(book_id=uuid.UUID(book_id),
                            quantity=row["quantity"], date=date.today())
        session.add(store_entry)
        await session.commit()


async def process_txt_data(session, file):
    content = await file.read()
    file_content = content.decode("utf-8")
    splitted_content = file_content.split("\n")

    structured_data = list()
    for line in splitted_content:
        line = line.replace("\r", "")
        barcode = line[:3]
        quantity = line[3:]
        structured_data.append({"barcode": barcode, "quantity": int(quantity)})
    
    df = pd.DataFrame(structured_data)

     # barcode db validations
    df["barcode"] = df["barcode"].replace(',', '', regex=True)
    file_barcodes = df['barcode'].tolist()

    # check data in db using barcodes
    db_books = await session.execute(select(Book.id, Book.barcode).filter(Book.barcode.in_(file_barcodes)))
    db_books = db_books.fetchall()
    db_books_barcodes = {db_book[1]: db_book[0] for db_book in db_books}
    db_barcodes = set(db_books_barcodes.keys())

    # check for non-existant barcode
    missing_barcode_index = None
    missing_barcode = False
    for index, file_barcode in enumerate(file_barcodes):
        if file_barcode not in db_barcodes:
            missing_barcode_index = index + 1
            missing_barcode = True
            break

    if missing_barcode:
        raise HTTPException(status_code=400, detail=f"Invalid barcode value at row {missing_barcode_index}")

    # Ingest data into the database
    for index, row in df.iterrows():
        if not row["barcode"]:
            continue

        book_id = db_books_barcodes[row["barcode"]]
        store_entry = Store(book_id=uuid.UUID(book_id),
                            quantity=row["quantity"], date=date.today())
        session.add(store_entry)
        await session.commit()


@router.post("/add")
async def add_book_store_data(
    new_store: StoreCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Add book store data"""
    result = await add_store_quantity_for_book(session, new_store, add=True)

    return ""


@router.post("/remove")
async def add_book_store_data(
    new_store: StoreCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Add book store data"""
    result = await add_store_quantity_for_book(session, new_store, add=False)

    return ""


@router.post("/bulk")
async def add_bulk_book_store_data(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(deps.get_session),
):
    """Add bulk book store data"""
    # Check if the file is an Excel/Text file
    if (not file.filename.endswith('.xlsx')) and (not file.filename.endswith('.txt')):
        raise HTTPException(
            status_code=400, detail="Only Excel/Text files (.xlsx, .txt) are allowed.")

    if file.filename.endswith('.xlsx'):
        await process_excel_data(session, file)
    elif file.filename.endswith('.txt'):
        await process_txt_data(session, file)

    return {"message": "Data imported successfully"}
