import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Type, AsyncGenerator

import qqbot
from nonebot.config import Env, Config
from nonebot.drivers import (
    Request,
    Response,
    WebSocket,
    HTTPVersion,
    ForwardMixin,
    ForwardDriver,
    combine_driver,
)
from nonebot.drivers import WebSocket as BaseWebSocket
from nonebot.drivers._block_driver import BlockDriver
from nonebot.internal.driver import Driver
from nonebot.log import LoguruHandler
from nonebot.typing import overrides

from pkg.openapi import OpenAPI

logger = logging.Logger("botfaas driver", "INFO")
logger.addHandler(LoguruHandler())

try:
    import httpx
except ImportError:
    raise ImportError(
        "Please install httpx by using `pip install nonebot2[httpx]`"
    ) from None

try:
    from websockets.exceptions import ConnectionClosed
    from websockets.legacy.client import Connect, WebSocketClientProtocol
except ImportError:
    raise ImportError(
        "Please install websockets by using `pip install nonebot2[websockets]`"
    )


class Mixin(ForwardMixin):
    """BotFaaS Mixin"""

    def __init__(self, env: Env, config: Config):
        self._loop = None
        self.msg = asyncio.Queue()
        token, sandbox = OpenAPI()
        config.qqguild_bots = [{
            'id': token.app_id,
            'token': token.access_token,
            'secret': '',
            'intent': {'guild_message': True}
        }]
        if sandbox:
            config.qqguild_is_sandbox = 'true'
        else:
            config.qqguild_is_sandbox = 'false'

        super().__init__(env, config)

    @property
    @overrides(ForwardMixin)
    def type(self) -> str:
        return "botfaas"

    @overrides(ForwardMixin)
    async def request(self, setup: Request) -> Response:
        async with httpx.AsyncClient(
                http2=setup.version == HTTPVersion.H2,
                proxies=setup.proxy,
                follow_redirects=True,
        ) as client:
            response = await client.request(
                setup.method,
                str(setup.url),
                content=setup.content,
                data=setup.data,
                json=setup.json,
                files=setup.files,
                headers=tuple(setup.headers.items()),
                timeout=setup.timeout,
            )
            return Response(
                response.status_code,
                headers=response.headers,
                content=response.content,
                request=setup,
            )

    @overrides(ForwardMixin)
    @asynccontextmanager
    async def websocket(self, setup: Request) -> AsyncGenerator["WebSocket", None]:
        yield BotFaaS(setup, self.msg)

    @overrides(Driver)
    def run(self, *args, **kwargs):
        """启动 block driver"""
        loop = asyncio.get_event_loop()
        self._loop = loop
        loop.run_until_complete(self.serve())

    def putMsg(self, trigger: str, msg: str):
        if trigger == 'AT_MESSAGE_CREATE':
            self._loop.call_soon_threadsafe(
                self.msg.put_nowait,
                '{"op":0,"s":2,"t":"AT_MESSAGE_CREATE","d":' + msg + '}'
            )


class BotFaaS(BaseWebSocket):
    num = 0

    def __init__(self, request: Request, msg: asyncio.Queue):
        super().__init__(request=request)
        self.msg = msg

    @property
    @overrides(BaseWebSocket)
    def closed(self) -> bool:
        return True

    @overrides(BaseWebSocket)
    async def accept(self):
        raise NotImplementedError

    @overrides(BaseWebSocket)
    async def close(self, code: int = 1000, reason: str = ""):
        raise NotImplementedError

    @overrides(BaseWebSocket)
    async def send(self, data: str) -> None:
        return None

    @overrides(BaseWebSocket)
    async def receive(self) -> str:
        self.num += 1
        if self.num == 1:
            return '{"d":{"heartbeat_interval":41250},"op":10}'
        elif self.num == 2:
            me = qqbot.UserAPI(qqbot.Token(os.environ.get("APP_ID"), os.environ.get("APP_TOKEN")),
                               os.environ.get("SANDBOX_BOT") == "true").me()
            return '{"op":0,"s":1,"t":"READY","d":{"version":1,"session_id":"mock-session","user":{' \
                   '"id":"' + me.id + '",' \
                                      '"username":"' + me.username + '","bot":true},"shard":[0,1]}}'
        return await self.msg.get()

    @overrides(BaseWebSocket)
    async def receive_bytes(self) -> bytes:
        return bytes([])

    @overrides(BaseWebSocket)
    async def send_bytes(self, data: bytes) -> None:
        return None


Driver: Type[ForwardDriver] = combine_driver(BlockDriver, Mixin)  # type: ignore
"""BotFaaS Driver"""
