from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class AuthorsBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: datetime

    class Config:
        from_attributes = True

class BooksBase(BaseModel):
    id: int
    name: str
    author: str
    published_at: datetime