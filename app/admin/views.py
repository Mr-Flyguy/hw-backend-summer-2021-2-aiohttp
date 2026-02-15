from __future__ import annotations

from aiohttp import web
from aiohttp_session import get_session
from aiohttp_apispec import request_schema, response_schema

from app.admin.schemes import AdminLoginSchema, AdminSchema


class AdminLoginView(web.View):
    @request_schema(AdminLoginSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        data = self.request["data"]
        email = data["email"]
        password = data["password"]

        admin = await self.request.app.store.admins.authenticate(email=email, password=password)
        if not admin:
            raise web.HTTPForbidden()

        session = await get_session(self.request)
        session["admin_id"] = admin.id

        return web.json_response({"id": admin.id, "email": admin.email})


class AdminCurrentView(web.View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        admin = self.request.get("admin")
        if not admin:
            raise web.HTTPUnauthorized()
        return web.json_response({"id": admin.id, "email": admin.email})
