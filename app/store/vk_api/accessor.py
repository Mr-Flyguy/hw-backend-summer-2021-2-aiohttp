from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

import aiohttp

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import LongPollServer, Update, parse_updates


class VkApiAccessor(BaseAccessor):
    def __init__(self, app):
        super().__init__(app)
        self.session: Optional[aiohttp.ClientSession] = None
        self.longpoll: Optional[LongPollServer] = None

    async def connect(self, app):
        await super().connect(app)
        self.session = aiohttp.ClientSession()
        await self._get_long_poll_server()

    async def disconnect(self, app):
        # gracefully закрыть ClientSession
        if self.session and not self.session.closed:
            await self.session.close()
        self.session = None
        await super().disconnect(app)

    async def _api_call(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        assert self.session is not None
        cfg = self.app.config.vk
        url = f"https://api.vk.com/method/{method}"

        full_params = dict(params)
        full_params["access_token"] = cfg.token
        full_params["v"] = cfg.api_version

        async with self.session.get(url, params=full_params) as resp:
            return await resp.json()

    async def _get_long_poll_server(self) -> None:
        """
        запросить сервер для Long Polling и сохранить параметры в стейте accessor'а
        """
        cfg = self.app.config.vk
        data = await self._api_call("groups.getLongPollServer", {"group_id": cfg.group_id})

        response = data.get("response") or {}
        self.longpoll = LongPollServer(
            key=str(response.get("key")),
            server=str(response.get("server")),
            ts=str(response.get("ts")),
        )

    async def poll(self) -> List[Update]:
        """
        отправить long poll запрос и вернуть список Update
        """
        if not self.longpoll:
            await self._get_long_poll_server()

        assert self.session is not None
        assert self.longpoll is not None

        params = {
            "act": "a_check",
            "key": self.longpoll.key,
            "ts": self.longpoll.ts,
            "wait": 25,
        }

        async with self.session.get(self.longpoll.server, params=params) as resp:
            raw = await resp.json()

        # VK может вернуть failed, тогда надо обновить сервер/ts
        if "failed" in raw:
            await self._get_long_poll_server()
            return []

        # обновим ts
        if raw.get("ts") is not None:
            self.longpoll.ts = str(raw["ts"])

        return parse_updates(raw)

    async def send_message(self, user_id: int, text: str) -> None:
        """
        отправить сообщение в VkApi
        """
        if not text:
            text = " "

        await self._api_call(
            "messages.send",
            {
                "user_id": int(user_id),
                "random_id": 0,
                "message": text,
            },
        )
