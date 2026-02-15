from __future__ import annotations

import hashlib
import hmac
from typing import Optional

from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor


def _hash_password(password: str) -> str:
    # Для задания достаточно стабильного хэша.
    # Главное: не хранить пароль в открытом виде.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(_hash_password(password), password_hash)


class AdminAccessor(BaseAccessor):
    async def connect(self, app):
        await super().connect(app)

        # Создаём первого админа при старте (из config.yml) :contentReference[oaicite:15]{index=15}
        cfg = app.config.admin
        if not any(a.email == cfg.email for a in app.store.database.admins):
            admin = Admin(
                id=app.store.database.next_admin_id,
                email=cfg.email,
                password_hash=_hash_password(cfg.password),
            )
            app.store.database.next_admin_id += 1
            app.store.database.admins.append(admin)

    async def disconnect(self, app):
        await super().disconnect(app)

    async def get_by_id(self, admin_id: int) -> Optional[Admin]:
        for a in self.app.store.database.admins:
            if a.id == admin_id:
                return a
        return None

    async def get_by_email(self, email: str) -> Optional[Admin]:
        for a in self.app.store.database.admins:
            if a.email == email:
                return a
        return None

    async def authenticate(self, email: str, password: str) -> Optional[Admin]:
        admin = await self.get_by_email(email)
        if not admin:
            return None
        if not _verify_password(password, admin.password_hash):
            return None
        return admin
