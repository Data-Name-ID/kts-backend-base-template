import string

from email_validator import EmailNotValidError, validate_email

from app.core.config import StaticConfig


def validate_and_normalize_email(email: str) -> str:
    try:
        email_info = validate_email(email, check_deliverability=True)
    except EmailNotValidError as e:
        msg = "Недопустимый формат email адреса"
        raise ValueError(msg) from e

    return email_info.normalized


def validate_password(password: str) -> None:
    if len(password) < StaticConfig.PASSWORD_MIN_LENGTH:
        msg = (
            "Пароль должен содержать "
            f"не менее {StaticConfig.PASSWORD_MIN_LENGTH} символов"
        )
        raise ValueError(msg)

    if not any(c.isupper() for c in password):
        msg = "Пароль должен содержать хотя бы одну заглавную букву"
        raise ValueError(msg)

    if not any(c.islower() for c in password):
        msg = "Пароль должен содержать хотя бы одну строчную букву"
        raise ValueError(msg)

    if not any(c.isdigit() for c in password):
        msg = "Пароль должен содержать хотя бы одну цифру"
        raise ValueError(msg)

    if not any(c in string.punctuation for c in password):
        msg = (
            "Пароль должен содержать хотя бы один специальный символ "
            f"из {string.punctuation}"
        )
        raise ValueError(msg)
