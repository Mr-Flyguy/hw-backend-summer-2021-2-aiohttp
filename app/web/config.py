from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import yaml


@dataclass
class SessionConfig:
    # secret_key должен быть 32 url-safe base64-encoded bytes для EncryptedCookieStorage
    # (в задании лежит в config.yml)
    secret_key: str
    cookie_name: str = "AIOHTTP_SESSION"


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class VkConfig:
    token: str
    group_id: int
    api_version: str = "5.131"


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig
    vk: VkConfig


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_config(config_path: str) -> Config:
    raw = load_config(config_path)

    admin = AdminConfig(
        email=raw["admin"]["email"],
        password=raw["admin"]["password"],
    )

    session = SessionConfig(
        secret_key=raw["session"]["secret_key"],
        cookie_name=raw["session"].get("cookie_name", "AIOHTTP_SESSION"),
    )

    vk = VkConfig(
        token=raw["vk"]["token"],
        group_id=int(raw["vk"]["group_id"]),
        api_version=raw["vk"].get("api_version", "5.131"),
    )

    return Config(admin=admin, session=session, vk=vk)
