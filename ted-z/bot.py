from abc import ABC
from typing import Any

from .utils.opening import load_bot_settings

import aiohttp
import crescent
import hikari
import miru

CONFIG = load_bot_settings()


class Bot(crescent.Bot, ABC):
    def __init__(self) -> None:
        super().__init__(token=CONFIG["bot"]["token"], intents=hikari.Intents.ALL_UNPRIVILEGED)

        self.plugins.load_folder("ted-z.plugins")

        self._session: aiohttp.ClientSession | None = None

        miru.install(self)

    def session(self) -> aiohttp.ClientSession:
        if not self._session:
            raise AttributeError("Session has not been set yet.")
        return self._session

    async def start(self, *args: Any, **kwargs: Any) -> None:
        self._session = aiohttp.ClientSession()
        await super().start(*args, **kwargs)

    async def join(self) -> None:
        await super().join()
        if self._session and not self._session.closed:
            await self._session.close()
