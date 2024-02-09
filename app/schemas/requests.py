from datetime import datetime, date

from pydantic import BaseModel, EmailStr, validator, UUID4


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str


class AuthorCreateRequest(BaseRequest):
    name: str
    birth_date: date

    @validator("birth_date", pre=True)
    def parse_birth_date(cls, value):
        date_object = datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()

        # Check if the value is less than January 1, 1900
        if date_object < date(1900, 1, 1):
            # Raise a ValueError with the error message
            raise ValueError("birth_date cannot be before January 1, 1900.")

        return date_object


class BookCreateRequest(BaseRequest):
    title: str
    barcode: str
    publishing_year: int
    author: UUID4

    @validator("publishing_year", pre=True)
    def validate_publishing_year(cls, value):
        # Check if the value is less than 1900
        if value < 1900:
            # Raise a ValueError with the error message
            raise ValueError("publishing_year cannot be less than 1900")

        return value



class StoreCreateRequest(BaseRequest):
    barcode: str
    quantity: int

    @validator("quantity", pre=True)
    def validate_quantity(cls, value):
        # Check if the value is less than 1900
        if value <= 0:
            # Raise a ValueError with the error message
            raise ValueError("quantity should be greater than 0")

        return value