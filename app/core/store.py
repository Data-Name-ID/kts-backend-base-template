from app.core.config import Config


class Store:
    def __init__(self, *, config: Config) -> None:
        self.config = config

        # core
        from app.core.db import DatabaseAccessor

        self.db = DatabaseAccessor(self)

        # accessors
        from app.users.accessor import UserAccessor

        self.users = UserAccessor(self)
