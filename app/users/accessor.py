from sqlalchemy.dialects.postgresql import insert

from app.core.accessors import BaseAccessor
from app.users.models import UserModel


class UserAccessor(BaseAccessor):
    async def upsert_user(self, email: str) -> int:
        stmt = (
            insert(UserModel)
            .values(email=email)
        )
        stmt_update = stmt.on_conflict_do_update(
            index_elements=[UserModel.email],
            set_={
                UserModel.email.key: stmt.excluded.email,
            },
        ).returning(UserModel.id)

        return await self.store.db.scalar_one(stmt_update)
