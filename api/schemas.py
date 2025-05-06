from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class AuthorModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: datetime

    class Config:
        from_attributes = True

class BookModel(BaseModel):
    id: int
    name: str
    author: str
    published_at: datetime

class AuthorAddModel(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime

class BookAddModel(BaseModel):
    name: str
    author: str
    published_at: datetime
    serial_number: int

class AuthorUpdateModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None

class BookUpdateModel(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    serial_number: Optional[int] = None