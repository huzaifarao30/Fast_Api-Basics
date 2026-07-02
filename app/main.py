import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routers.books import router as books_router
from app.core.exceptions import DuplicateTitleError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("books_api")

app = FastAPI(title="Book Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000

    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.1f}ms)")
    response.headers["X-Process-Time-Ms"] = f"{duration_ms:.1f}"
    return response


app.include_router(books_router)


@app.exception_handler(DuplicateTitleError)
def duplicate_title_handler(request: Request, exc: DuplicateTitleError):
    return JSONResponse(
        status_code=409,
        content={"error": "duplicate_title", "detail": f"'{exc.title}' already exists"},
    )

