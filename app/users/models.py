from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import StaticConfig
from app.core.db import BaseModel
from app.core.models.mixins import CreatedAtMixin, IDMixin, UpdatedAtMixin


class UserModel(IDMixin, CreatedAtMixin, UpdatedAtMixin, BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(StaticConfig.CREDENTIALS_STR_LENGTH),
        unique=True,
    )

    activated: Mapped[bool] = mapped_column(default=False)
