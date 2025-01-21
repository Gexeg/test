from dataclasses import dataclass


@dataclass
class Settings:
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    SITE_HOST: str = "http://0.0.0.0:8000"
    LOG_LEVEL: int = 10


def parse_config() -> Settings:
    return Settings()


settings = parse_config()
