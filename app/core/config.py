import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Loyihaning asosiy ildiz yo'li
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Birlamchi bot tokeni (.env dan olinadi)
DEFAULT_BOT_TOKEN = os.getenv("BOT_TOKEN", "")


class Settings(BaseSettings):
    """
    Bot konfiguratsiyasi.
    """
    # Telegram Bot Token (@BotFather dan)
    bot_token: str = Field(default=DEFAULT_BOT_TOKEN, alias="BOT_TOKEN")

    # Antiflood (so'rovlar orasidagi minimal vaqt, sekundda)
    rate_limit: float = Field(default=1.5, alias="RATE_LIMIT")

    # Logging darajasi
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


try:
    settings = Settings()
except Exception:
    class FallbackSettings(BaseSettings):
        bot_token: str = os.getenv("BOT_TOKEN", DEFAULT_BOT_TOKEN)
        rate_limit: float = float(os.getenv("RATE_LIMIT", "1.5"))
        log_level: str = os.getenv("LOG_LEVEL", "INFO")
        model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    settings = FallbackSettings()
