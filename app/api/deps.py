from fastapi import Depends, HTTPException

from app.core.database import get_db


class Pagination:
    def __init__(self, skip: int = 0, limit: int = 20):
        self.skip = skip
        self.limit = limit


def get_book_or_404(book_id: int, db=Depends(get_db)):
    book = db.find_one({"id": book_id})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
