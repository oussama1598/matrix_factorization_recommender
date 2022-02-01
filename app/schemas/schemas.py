from pydantic.main import BaseModel


class BookRating(BaseModel):
    book_id: int
    rating: float


class BookData(BaseModel):
    title: str
    image_url: str


class Book(BookData):
    rating: float
