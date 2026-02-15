from __future__ import annotations

from aiohttp import web
from aiohttp_session import get_session


@web.middleware
async def auth_middleware(request: web.Request, handler):
    """
    Достаём admin из session cookie (если есть) и кладём в request["admin"].
    """
    request["admin"] = None

    session = await get_session(request)
    admin_id = session.get("admin_id")
    if admin_id is not None:
        admin = await request.app.store.admins.get_by_id(int(admin_id))
        request["admin"] = admin

    return await handler(request)
