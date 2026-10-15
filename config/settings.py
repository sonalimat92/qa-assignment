import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://qae-assignment-tau.vercel.app").rstrip("/")
    user_id: str = os.getenv("USER_ID", "")
    headless: bool = _as_bool(os.getenv("HEADLESS", "true"))
    explicit_wait_seconds: int = int(os.getenv("EXPLICIT_WAIT_SECONDS", "10"))
    api_timeout_seconds: int = int(os.getenv("API_TIMEOUT_SECONDS", "15"))
    chrome_binary: str = os.getenv("CHROME_BINARY", "")
    chromedriver_path: str = os.getenv("CHROMEDRIVER_PATH", "")
    chrome_args: str = os.getenv("CHROME_ARGS", "")


settings = Settings()
