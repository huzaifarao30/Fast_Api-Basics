from typing import List

from fastapi import APIRouter, Depends, status

from app.api.deps import Pagination, get_book_or_404
from app.core.database import get_db
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookResponse])
def list_books(db=Depends(get_db), page: Pagination = Depends(Pagination)):
    return db[page.skip : page.skip + page.limit]


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book: dict = Depends(get_book_or_404)):
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db=Depends(get_db)):
    new_book = {"id": len(db) + 1, "title": book.title, "author": book.author}
    db.append(new_book)
    return new_book


@router.patch("/{book_id}", response_model=BookResponse)
def update_book(book_update: BookUpdate, book: dict = Depends(get_book_or_404)):
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            book[key] = value
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book: dict = Depends(get_book_or_404), db=Depends(get_db)):
    db.remove(book)
    return None

