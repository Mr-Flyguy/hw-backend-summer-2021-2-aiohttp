from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Admin:
    id: int
    email: str
    password_hash: str
