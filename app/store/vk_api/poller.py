from __future__ import annotations

import asyncio
from typing import Optional

from app.base.base_accessor import BaseAccessor


class Poller(BaseAccessor):
    def __init__(self, app):
        super().__init__(app)
        self._task: Optional[asyncio.Task] = None
        self._stopping = asyncio.Event()

    async def poll(self):
        """
        пока Poller не остановлен вызывает vk_api.poll и если пришли апдейты —
        отправляет их в bot_manager.handle_updates
        """
        self._stopping.clear()
        while not self._stopping.is_set():
            updates = await self.app.store.vk_api.poll()
            if updates:
                await self.app.store.bot_manager.handle_updates(updates)

    async def start(self):
        """
        запускает poll через asyncio.create_task и сохраняет задачу
        """
        if self._task and not self._task.done():
            return
        self._task = asyncio.create_task(self.poll())

    async def stop(self):
        """
        gracefully завершает Poller: ждёт завершения текущего poll-цикла
        """
        self._stopping.set()
        if self._task:
            await self._task
        self._task = None
