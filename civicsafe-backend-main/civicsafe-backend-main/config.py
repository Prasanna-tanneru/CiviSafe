from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    CORS_ORIGINS: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    HASHING_SCHEME: str = "pbkdf2_sha256"
    API_URL: str = "http://localhost:8000"
    ANALYTICS_EXCEL_PATH: str = "analytics/analytics.xlsx"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
