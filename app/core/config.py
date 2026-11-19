import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    bot_token: str = Field(default="", alias="BOT_TOKEN")
    rate_limit: float = Field(default=1.5, alias="RATE_LIMIT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


try:
    settings = Settings()
except Exception:
    class FallbackSettings:
        bot_token: str = os.environ.get("BOT_TOKEN", "")
        rate_limit: float = float(os.environ.get("RATE_LIMIT", "1.5"))
        log_level: str = os.environ.get("LOG_LEVEL", "INFO")

    settings = FallbackSettings()
