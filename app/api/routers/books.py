import re
from typing import List

from fastapi import APIRouter, Depends, status

from app.api.deps import Pagination, get_book_or_404
from app.core.database import get_db
from app.core.exceptions import DuplicateTitleError
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookResponse])
def list_books(db=Depends(get_db), page: Pagination = Depends(Pagination)):
    return list(db.find().skip(page.skip).limit(page.limit))


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book: dict = Depends(get_book_or_404)):
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db=Depends(get_db)):
    existing_book = db.find_one({"title": {"$regex": f"^{re.escape(book.title)}$", "$options": "i"}})
    if existing_book:
        raise DuplicateTitleError(title=book.title)

    last_book = db.find_one(sort=[("id", -1)])
    next_id = (last_book["id"] + 1) if last_book else 1

    new_book = {"id": next_id, "title": book.title, "author": book.author}
    db.insert_one(new_book)
    return new_book


@router.patch("/{book_id}", response_model=BookResponse)
def update_book(book_update: BookUpdate, book: dict = Depends(get_book_or_404), db=Depends(get_db)):
    update_data = book_update.model_dump(exclude_unset=True)
    if not update_data:
        return book

    for key, value in update_data.items():
        if value is not None:
            book[key] = value

    db.update_one({"_id": book["_id"]}, {"$set": update_data})
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book: dict = Depends(get_book_or_404), db=Depends(get_db)):
    db.delete_one({"_id": book["_id"]})
    return None


