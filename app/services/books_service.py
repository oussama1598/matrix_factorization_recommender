import json
import os

from app.schemas.schemas import BookData

with open(os.path.join(os.getcwd(), './data/books.json'), 'r') as file:
    books = json.load(file)


def get_book_data(book_id: str) -> BookData:
    return BookData(**books[book_id])
