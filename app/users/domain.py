from msgspec import Struct


class UserAuth(Struct, kw_only=True, frozen=True):
    id: int
