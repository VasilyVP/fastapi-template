from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import FastAPI
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI Template"
    admin_email: str | None = None
    items_per_user: int = 50
    database_url: str = Field(min_length=1)

    secret_key: str = Field(min_length=1)
    algorithm: str = Field(min_length=1)
    access_token_expire_minutes: int = Field(gt=0)
    refresh_token_expire_days: int = Field(default=30, gt=0)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Force settings validation at startup.
    get_settings()
    from sqlmodel import Session

    from app.db.seed import seed_demo_data
    from app.db.session import create_db_and_tables, engine

    create_db_and_tables()
    with Session(engine) as session:
        seed_demo_data(session)
    yield
