from pydantic import BaseSettings


class Settings(BaseSettings):
    DATASET_PATH: str
    BOOKS_DIR: str

    class Config:
        env_file = '../.env'


settings = Settings()
