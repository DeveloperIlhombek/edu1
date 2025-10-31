from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:Ilhom1215@localhost:5433/edusystem"
    JWT_SECRET_KEY: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    BOT_TOKEN: str="8497951622:AAG6Ry4k6sQoF0O2geWMyZsHPYxQRraW2y0"

    class Config:
        env_file = ".env"
settings = Settings()










































