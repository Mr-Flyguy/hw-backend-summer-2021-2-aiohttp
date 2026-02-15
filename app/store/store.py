from __future__ import annotations

from aiohttp.web_app import Application

from app.store.database.database import Database
from app.store.admin.accessor import AdminAccessor
from app.store.quiz.accessor import QuizAccessor
from app.store.vk_api.accessor import VkApiAccessor
from app.store.vk_api.poller import Poller
from app.store.bot.manager import BotManager


class Store:
    def __init__(self, app: Application):
        self.app = app
        self.database = Database()

        self.admins = AdminAccessor(app)
        self.quizzes = QuizAccessor(app)
        self.vk_api = VkApiAccessor(app)
        self.poller = Poller(app)
        self.bot_manager = BotManager(app)

    async def connect(self, app: Application):
        await self.admins.connect(app)
        await self.quizzes.connect(app)
        await self.vk_api.connect(app)
        await self.poller.connect(app)
        await self.bot_manager.connect(app)

        # Автостарт longpoll
        await self.poller.start()

    async def disconnect(self, app: Application):
        await self.poller.stop()

        await self.bot_manager.disconnect(app)
        await self.poller.disconnect(app)
        await self.vk_api.disconnect(app)
        await self.quizzes.disconnect(app)
        await self.admins.disconnect(app)
