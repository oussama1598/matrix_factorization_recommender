from fastapi import APIRouter

from app.api.endpoints import ratings
from app.services import books_service

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(ratings.router)


@router.get('/')
async def index():
    return books_service.get_book_data('8601')
