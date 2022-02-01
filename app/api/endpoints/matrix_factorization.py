from typing import List

import fastapi

from app.schemas.schemas import BookRating, Book
from app.services import recommender_service, books_service

router = fastapi.APIRouter(
    prefix='/matrix_factorization'
)


@router.get('/{user_id}/top/{top_n}', response_model=List[Book])
async def ratings_index(user_id: int, top_n: int):
    books: List[Book] = []
    books_rating: List[BookRating] = recommender_service.get_recommender('matrix_factorization').get_top_n(user_id,
                                                                                                           top_n)

    for book_rating in books_rating:
        book_data = books_service.get_book_data(str(book_rating.book_id))

        books.append(
            Book(
                title=book_data.title,
                image_url=book_data.image_url,
                rating=book_rating.rating
            )
        )

    return books
