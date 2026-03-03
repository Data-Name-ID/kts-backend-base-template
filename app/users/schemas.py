from msgspec import Struct

from app.core import validators


class UserEmailRequest(Struct, kw_only=True):
    email: str

    def __post_init__(self) -> None:
        self.email = validators.validate_and_normalize_email(self.email)
