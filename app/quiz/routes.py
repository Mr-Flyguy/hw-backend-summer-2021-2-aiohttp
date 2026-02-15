from __future__ import annotations

from aiohttp import web

from app.quiz.views import (
    QuizAddQuestionView,
    QuizAddThemeView,
    QuizListQuestionsView,
    QuizListThemesView,
)


def setup_routes(app: web.Application):
    app.router.add_view("/quiz.add_theme", QuizAddThemeView)
    app.router.add_view("/quiz.list_themes", QuizListThemesView)
    app.router.add_view("/quiz.add_question", QuizAddQuestionView)
    app.router.add_view("/quiz.list_questions", QuizListQuestionsView)
