from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    allowed_origins: str = "http://127.0.0.1:5500,http://localhost:5500"
    data_dir: str = "./data"
    model_name: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"
    max_chunk_size: int = 900
    chunk_overlap: int = 150
    top_k: int = 4

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("data_dir")
    @classmethod
    def validate_data_dir(cls, value: str) -> str:
        Path(value).mkdir(parents=True, exist_ok=True)
        return value

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
