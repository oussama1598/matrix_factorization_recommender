from typing import List

import fastapi

from app.schemas.ratings_schemas import BookRating
from app.services import recommender_service

router = fastapi.APIRouter(
    prefix='/ratings'
)


@router.get('/{user_id}/top/{top_n}', response_model=List[BookRating])
async def ratings_index(user_id: int, top_n: int):
    return recommender_service.get_recommender('matrix_factorization').get_top_n(user_id, top_n)
