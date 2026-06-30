from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "StockWise API"
    PROJECT_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()