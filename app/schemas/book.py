from typing import Optional

from pydantic import BaseModel, Field, field_validator


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)

    @field_validator("title", "author")
    @classmethod
    def strip_and_check_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty or only whitespace")
        return value



class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
