from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Theme:
    id: int
    title: str


@dataclass
class Answer:
    title: str
    is_correct: bool


@dataclass
class Question:
    id: int
    title: str
    theme_id: int
    answers: List[Answer]
