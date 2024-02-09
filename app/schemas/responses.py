from datetime import datetime, date

from pydantic import BaseModel, ConfigDict, EmailStr, UUID4


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class UserResponse(BaseResponse):
    id: str
    email: EmailStr


class AuthorResponse(BaseResponse):
    id: UUID4
    name: str
    birth_date: date

class BookResponse(BaseResponse):
    id: UUID4
    title: str
    barcode: str
    publishing_year: int
    quantity: int
    author: AuthorResponse