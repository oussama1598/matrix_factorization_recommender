from pydantic.main import BaseModel


class BookRating(BaseModel):
    book_id: int
    rating: float
