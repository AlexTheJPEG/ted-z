from abc import ABC

import aiohttp
import hikari
import crescent
import tomli

from typing import Any

with open("bot_settings.toml", mode="rb") as fp:
    config = tomli.load(fp)


class Bot(crescent.Bot, ABC):
    def __init__(self) -> None:
        super().__init__(
            token=config["bot"]["token"],
            intents=hikari.Intents.ALL_UNPRIVILEGED
        )

        self._session: aiohttp.ClientSession | None = None

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
