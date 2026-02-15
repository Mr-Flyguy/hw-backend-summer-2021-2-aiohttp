from __future__ import annotations

from typing import List

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Update


class BotManager(BaseAccessor):
    async def handle_updates(self, updates: List[Update]) -> None:
        """
        По ТЗ: на каждое новое сообщение пользователя — отправить непустое сообщение. :contentReference[oaicite:19]{index=19}
        Важно: не менять имя/место/сигнатуру — в тестах подменяют. :contentReference[oaicite:20]{index=20}
        """
        for upd in updates:
            if not upd.message:
                continue
            await self.app.store.vk_api.send_message(
                user_id=upd.message.user_id,
                text="Привет! Сообщение получено ✅",
            )
