from fastapi import APIRouter

from app.api.endpoints import authors, health, books, stores, history

api_router = APIRouter()
api_router.include_router(authors.router, prefix="/author", tags=["authors"])
api_router.include_router(books.router, prefix="/book", tags=["books"])
api_router.include_router(stores.router, prefix="/leftovers", tags=["store"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
