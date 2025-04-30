from typing import Optional, List
from pydantic import BaseModel

class UserBase(BaseModel):
    class Config:
        orm_mode = True