from collections.abc import Sequence

from litestar.types import ControllerRouterHandler

from app.users.views import UserController


def get_handlers() -> Sequence[ControllerRouterHandler]:
    return (UserController,)
