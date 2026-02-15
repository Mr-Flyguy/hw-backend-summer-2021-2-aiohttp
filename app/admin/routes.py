from __future__ import annotations

from aiohttp import web

from app.admin.views import AdminLoginView, AdminCurrentView


def setup_routes(app: web.Application):
    app.router.add_view("/admin.login", AdminLoginView)
    app.router.add_view("/admin.current", AdminCurrentView)
