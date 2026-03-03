from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.config.app import AppConfig
from litestar.datastructures import State
from litestar.di import Provide
from litestar.logging import LoggingConfig, StructLoggingConfig
from litestar.plugins import InitPlugin as LitestarInitPlugin
from litestar.types import Dependencies

from app.core.store import Store

_APP_STATE_STORE = "store"


class InitPlugin(LitestarInitPlugin):
    def __init__(
        self,
        *,
        app_name: str,
        app_version: str,
        store: Store,
    ) -> None:
        self._app_name = app_name
        self._app_version = app_version
        self._store = store

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.lifespan.insert(0, self._store_lifespan)
        app_config.dependencies.update(self.default_dependencies())
        app_config.logging_config = self.default_logging_config()

        return app_config

    def default_dependencies(self) -> Dependencies:
        return {
            "store": Provide(self.state_get_store, sync_to_thread=False),
        }

    @staticmethod
    def state_get_store(state: State) -> Store | None:
        return getattr(state, _APP_STATE_STORE, None)

    @asynccontextmanager
    async def _store_lifespan(self, app: Litestar) -> AsyncGenerator[None, None]:
        setattr(app.state, _APP_STATE_STORE, self._store)
        await self._store.db.connect()
        yield

    @staticmethod
    def default_logging_config() -> StructLoggingConfig:
        return StructLoggingConfig(
            standard_lib_logging_config=LoggingConfig(
                disable_existing_loggers=False,
                incremental=False,
                configure_root_logger=False,
                log_exceptions="debug",
            ),
            pretty_print_tty=True,
        )
