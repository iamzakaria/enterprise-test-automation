"""Validated environment configuration; never log credentials or target URLs."""

from dataclasses import dataclass
from typing import Mapping
from urllib.parse import urlsplit


@dataclass(frozen=True)
class Settings:
    environment: str
    base_url: str | None
    timeout_ms: int

    @classmethod
    def from_env(cls, env: Mapping[str, str]) -> "Settings":
        environment = env.get("TEST_ENV", "local").strip().lower()
        if environment not in {"local", "qa", "staging"}:
            raise ValueError("TEST_ENV must be local, qa, or staging")
        base_url = env.get("BASE_URL", "").strip() or None
        if base_url:
            try:
                parsed = urlsplit(base_url)
                valid = (
                    parsed.scheme in {"http", "https"}
                    and parsed.hostname
                    and not parsed.username
                    and not parsed.password
                    and not parsed.query
                    and not parsed.fragment
                )
                _ = parsed.port
            except ValueError:
                valid = False
            if not valid:
                raise ValueError(
                    "BASE_URL must be HTTP(S), without credentials, query, or fragment"
                )
        if environment != "local" and not base_url:
            raise ValueError("BASE_URL is required for qa and staging")
        try:
            timeout = int(env.get("UI_TIMEOUT_MS", "5000"))
        except ValueError as exc:
            raise ValueError("UI_TIMEOUT_MS must be a positive integer") from exc
        if timeout <= 0:
            raise ValueError("UI_TIMEOUT_MS must be a positive integer")
        return cls(environment, base_url, timeout)
