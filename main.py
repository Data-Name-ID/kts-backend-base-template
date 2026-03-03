from typing import Any

from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.connection import ASGIConnection
from litestar.datastructures import State
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.openapi.spec.license import License
from litestar.security.jwt import JWTAuth, Token

import app.users.urls as users_urls
from app.core.config import create_config
from app.core.store import Store
from app.users.domain import UserAuth
from app.web.plugins import InitPlugin

config = create_config()
store = Store(config=config)


def retrieve_user_handler(
    token: Token,
    _: ASGIConnection[Any, Any, Any, Any],
) -> UserAuth:
    return UserAuth(id=int(token.sub))


jwt_auth = JWTAuth[UserAuth](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=config.security.jwt.token_secret,
    default_token_expiration=config.security.jwt.token_expiration,
    exclude=["/docs", "/openapi.json"],
)


app = Litestar(
    route_handlers=(*users_urls.get_handlers(),),
    on_app_init=[
        jwt_auth.on_app_init,
    ],
    state=State(
        {
            "jwt_auth": jwt_auth,
        },
    ),
    plugins=(
        InitPlugin(
            app_name="api",
            app_version="1.0.0",
            store=store,
        ),
    ),
    cors_config=CORSConfig(allow_origins=config.security.cors_allowed_origins),
    openapi_config=OpenAPIConfig(
        title="api",
        path="/docs",
        version="1.0.0",
        root_schema_site="swagger",
        license=License(
            name="MIT",
            url="https://opensource.org/licenses/MIT",
            identifier="MIT",
        ),
        render_plugins=[ScalarRenderPlugin()],
    ),
)
