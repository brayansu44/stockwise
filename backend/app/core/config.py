from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "StockWise API"
    PROJECT_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()