from typing import List

import fastapi

from app.schemas.schemas import Book
from app.services import recommender_service, books_service

router = fastapi.APIRouter(
    prefix='/items'
)


@router.get('/{book_id}/top', response_model=List[Book])
async def ratings_index(book_id: int):
    books: List[Book] = []
    books_ids: List[int] = recommender_service.get_recommender('knn').get_top_n(book_id)

    for book_id in books_ids:
        book_data = books_service.get_book_data(str(book_id))

        books.append(
            Book(
                title=book_data.title,
                image_url=book_data.image_url
            )
        )

    return books
