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


    

