from fastapi import APIRouter

from app.api.endpoints import ratings

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(ratings.router)


@router.get('/')
async def index():
    return 'OK'
