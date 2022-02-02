from pydantic import BaseSettings


class Settings(BaseSettings):
    DATASET_PATH: str
    BOOKS_PATH: str
    TAGS_PATH: str
    BOOK_TAGS_PATH: str

    class Config:
        env_file = '../.env'


settings = Settings()
