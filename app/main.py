from fastapi import FastAPI

from app.api.routers.books import router as books_router

app = FastAPI(title="Book Management API")

app.include_router(books_router)
