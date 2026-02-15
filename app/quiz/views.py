from __future__ import annotations

from aiohttp import web
from aiohttp_apispec import request_schema, response_schema

from app.quiz.schemes import (
    QuestionCreateSchema,
    QuestionListSchema,
    QuestionSchema,
    ThemeCreateSchema,
    ThemeListSchema,
    ThemeSchema,
)


class QuizAddThemeView(web.View):
    @request_schema(ThemeCreateSchema)
    @response_schema(ThemeSchema, 200)
    async def post(self):
        if not self.request.get("admin"):
            raise web.HTTPUnauthorized()

        data = self.request["data"]
        try:
            theme = await self.request.app.store.quizzes.add_theme(title=data["title"])
        except ValueError:
            raise web.HTTPConflict()

        return web.json_response({"id": theme.id, "title": theme.title})


class QuizListThemesView(web.View):
    @response_schema(ThemeListSchema, 200)
    async def get(self):
        if not self.request.get("admin"):
            raise web.HTTPUnauthorized()

        themes = await self.request.app.store.quizzes.list_themes()
        return web.json_response({"themes": [{"id": t.id, "title": t.title} for t in themes]})


class QuizAddQuestionView(web.View):
    @request_schema(QuestionCreateSchema)
    @response_schema(QuestionSchema, 200)
    async def post(self):
        if not self.request.get("admin"):
            raise web.HTTPUnauthorized()

        data = self.request["data"]
        try:
            q = await self.request.app.store.quizzes.add_question(
                title=data["title"],
                theme_id=int(data["theme_id"]),
                answers=list(data["answers"]),
            )
        except LookupError:
            raise web.HTTPNotFound()
        except ValueError as e:
            # conflict / bad_request разделяем по смыслу
            if str(e) == "question_exists":
                raise web.HTTPConflict()
            raise web.HTTPBadRequest()

        return web.json_response(
            {
                "id": q.id,
                "title": q.title,
                "theme_id": q.theme_id,
                "answers": [{"title": a.title, "is_correct": a.is_correct} for a in q.answers],
            }
        )


class QuizListQuestionsView(web.View):
    @response_schema(QuestionListSchema, 200)
    async def get(self):
        if not self.request.get("admin"):
            raise web.HTTPUnauthorized()

        theme_id = self.request.query.get("theme_id")
        theme_id_int = int(theme_id) if theme_id is not None else None

        questions = await self.request.app.store.quizzes.list_questions(theme_id=theme_id_int)
        return web.json_response(
            {
                "questions": [
                    {
                        "id": q.id,
                        "title": q.title,
                        "theme_id": q.theme_id,
                        "answers": [{"title": a.title, "is_correct": a.is_correct} for a in q.answers],
                    }
                    for q in questions
                ]
            }
        )
