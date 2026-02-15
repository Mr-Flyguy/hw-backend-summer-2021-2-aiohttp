from __future__ import annotations

from typing import List, Optional

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Answer, Question, Theme


class QuizAccessor(BaseAccessor):
    async def add_theme(self, title: str) -> Theme:
        # уникальность темы
        for t in self.app.store.database.themes:
            if t.title == title:
                raise ValueError("theme_exists")

        theme = Theme(id=self.app.store.database.next_theme_id, title=title)
        self.app.store.database.next_theme_id += 1
        self.app.store.database.themes.append(theme)
        return theme

    async def list_themes(self) -> List[Theme]:
        return list(self.app.store.database.themes)

    async def get_theme(self, theme_id: int) -> Optional[Theme]:
        for t in self.app.store.database.themes:
            if t.id == theme_id:
                return t
        return None

    async def add_question(self, title: str, theme_id: int, answers: List[dict]) -> Question:
        # тема должна существовать (иначе 404) :contentReference[oaicite:16]{index=16}
        theme = await self.get_theme(theme_id)
        if not theme:
            raise LookupError("theme_not_found")

        # уникальность вопроса -> 409 :contentReference[oaicite:17]{index=17}
        for q in self.app.store.database.questions:
            if q.title == title:
                raise ValueError("question_exists")

        # валидации ответов (400):
        # 1) минимум 2 ответа
        if len(answers) < 2:
            raise ValueError("need_multiple_answers")

        # 2) ровно 1 correct
        correct_count = sum(1 for a in answers if a.get("is_correct") is True)
        if correct_count == 0:
            raise ValueError("need_correct_answer")
        if correct_count > 1:
            raise ValueError("only_one_correct")

        ans_models = [Answer(title=a["title"], is_correct=bool(a["is_correct"])) for a in answers]
        q = Question(
            id=self.app.store.database.next_question_id,
            title=title,
            theme_id=theme_id,
            answers=ans_models,
        )
        self.app.store.database.next_question_id += 1
        self.app.store.database.questions.append(q)
        return q

    async def list_questions(self, theme_id: Optional[int] = None) -> List[Question]:
        if theme_id is None:
            return list(self.app.store.database.questions)
        return [q for q in self.app.store.database.questions if q.theme_id == theme_id]
