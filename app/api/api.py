from fastapi import APIRouter

from app.api.endpoints import knn_item, knn_user, matrix_factorization, knn_content
from app.services import books_service

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(matrix_factorization.router)
router.include_router(knn_user.router)
router.include_router(knn_item.router)
router.include_router(knn_content.router)


@router.get('/')
async def index():
    return books_service.get_book_data('8601')
