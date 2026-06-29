from typing import Optional

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
