from typing import List

from fastapi import APIRouter, HTTPException, status

from app.core.database import fake_db
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookResponse])
def list_books():
    return fake_db


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    for book in fake_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    new_book = {"id": len(fake_db) + 1, "title": book.title, "author": book.author}
    fake_db.append(new_book)
    return new_book


@router.patch("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate):
    for book in fake_db:
        if book["id"] == book_id:
            update_data = (
                book_update.model_dump(exclude_unset=True)
            )
            for key, value in update_data.items():
                if value is not None:
                    book[key] = value
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    for index, book in enumerate(fake_db):
        if book["id"] == book_id:
            fake_db.pop(index)
            return None
    raise HTTPException(status_code=404, detail="Book not found")
