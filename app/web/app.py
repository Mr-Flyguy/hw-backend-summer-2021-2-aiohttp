from __future__ import annotations

import base64
from typing import Optional

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from app.store.store import Store
from app.web.config import Config, setup_config
from app.web.logger import setup_logging
from app.web.auth import auth_middleware
from app.web.middlewares import error_middleware
from app.web.routes import setup_routes


class Application(web.Application):
    config: Config
    store: Store


def setup_session_storage(app: Application) -> None:
    # EncryptedCookieStorage ждёт bytes ключ
    # config.yml обычно хранит urlsafe base64 строку
    secret = base64.urlsafe_b64decode(app.config.session.secret_key.encode("utf-8"))
    storage = EncryptedCookieStorage(secret_key=secret, cookie_name=app.config.session.cookie_name)
    setup_session(app, storage)


def setup_app(config_path: str) -> Application:
    app = Application(middlewares=[error_middleware])

    app.config = setup_config(config_path)
    setup_logging(app)

    # swagger_dict + validation_middleware (aiohttp-apispec)
    setup_aiohttp_apispec(app, title="KTS Quiz Bot", version="1.0.0")

    setup_session_storage(app)

    app.store = Store(app)
    app.on_startup.append(app.store.connect)
    app.on_cleanup.append(app.store.disconnect)

    setup_routes(app)
    return app
