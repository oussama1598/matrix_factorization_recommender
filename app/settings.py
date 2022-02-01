from pydantic import BaseSettings


class Settings(BaseSettings):
    DATASET_PATH: str
    MODELS_DIR: str

    class Config:
        env_file = '../.env'


settings = Settings()
