from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.admin.models import Admin
from app.quiz.models import Question, Theme


@dataclass
class Database:
    admins: List[Admin] = field(default_factory=list)
    themes: List[Theme] = field(default_factory=list)
    questions: List[Question] = field(default_factory=list)

    next_admin_id: int = 1
    next_theme_id: int = 1
    next_question_id: int = 1
