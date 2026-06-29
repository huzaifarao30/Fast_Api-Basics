from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id:  int
    title: str
    author: str

fake_db = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin"}
]

@app.get("/")
def home():
    return {"message" : "Book Api is running"}

@app.get("/books")
def get_all_books():
    return fake_db

@app.get("/books/{book_id}")
def get_book(book_id : int):
    for book in fake_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404 ,detail="Book not found")

@app.post("/books")
def create_book(new_book : Book):
    fake_db.append(new_book.model_dump())

    return {"message" : f"Successfully added '{new_book.title}'!"}

@app.delete("/books/{book_id}")
def delete_book(book_id : int):
    for index, book in enumerate(fake_db):
        if book["id"] == book_id:
            deleted_book = fake_db.pop(index)
            return {"message": f"Successfully deleted '{deleted_book['title']}'"}
            
    raise HTTPException(status_code=404, detail="Book not found to delete")


@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(fake_db):
        if book["id"] == book_id:
            fake_db[index] = updated_book.model_dump()  
            return {"message": f"Successfully updated book ID {book_id}!"}

    raise HTTPException(status_code=404, detail="Book not found to update")