from msgspec import Struct


class OkResponse[T: Struct](Struct):
    status: str = "ok"
    data: T | None = None
