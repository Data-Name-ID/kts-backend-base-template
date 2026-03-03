from datetime import timedelta

import msgspec
from dynaconf import Dynaconf
from sqlalchemy.engine.url import URL


class StaticConfig:
    USERNAME_MIN_LENGTH = 3
    PASSWORD_MIN_LENGTH = 8

    SHORT_STR_LENGTH = 20  # Коды, статусы, идентификаторы
    NAME_STR_LENGTH = 100  # Имена, логины, названия, заголовки, теги
    DESCRIPTION_STR_LENGTH = 500  # Краткие описания, аннотации, комментарии
    LONG_STR_LENGTH = 1000  # Длинные тексты, описания, аннотации
    URL_STR_LENGTH = 2048  # Ссылки, адреса, пути
    CREDENTIALS_STR_LENGTH = 255  # Email-адреса, пароли


class DatabaseConfig(msgspec.Struct, kw_only=True, frozen=True):
    user: str | None = "postgres"
    password: str | None = "postgres"  # noqa: S105
    host: str = "localhost"
    port: int = 5432
    name: str = "postgres"

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )


class JWTConfig(msgspec.Struct, kw_only=True, frozen=True):
    token_secret: str
    token_expiration_minutes: int = 60 * 24  # 24 hours

    @property
    def token_expiration(self) -> timedelta:
        return timedelta(minutes=self.token_expiration_minutes)


class SecurityConfig(msgspec.Struct, kw_only=True, frozen=True):
    cors_allowed_origins: list[str] = msgspec.field(
        default_factory=lambda: [
            "http://localhost",
            "http://localhost:8000",
        ],
    )
    jwt: JWTConfig


class Config(msgspec.Struct, kw_only=True, frozen=True):
    db: DatabaseConfig
    security: SecurityConfig


def create_config() -> Config:
    config_raw = Dynaconf(settings_files=[".secrets.yaml"]).as_dict()
    config_raw = {k.lower(): v for k, v in config_raw.items()}
    return msgspec.convert(config_raw, type=Config)
