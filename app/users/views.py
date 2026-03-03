from typing import TYPE_CHECKING, cast

from litestar import Controller, Request, post, status_codes

if TYPE_CHECKING:
    from litestar.security.jwt import JWTAuth

from app.core.schemas import OkResponse
from app.core.store import Store
from app.users.schemas import UserEmailRequest


class UserController(Controller):
    path = "/api/users"
    tags = ("users",)

    @post(
        path="login",
        status_code=status_codes.HTTP_200_OK,
        exclude_from_auth=True,
    )
    async def auth(
        self,
        store: Store,
        request: Request,
        data: UserEmailRequest,
    ) -> OkResponse:
        user_id = await store.users.upsert_user(email=data.email)

        jwt_auth = cast("JWTAuth", request.app.state["jwt_auth"])
        token = jwt_auth.create_token(str(user_id))

        return OkResponse(data={"token": token})
