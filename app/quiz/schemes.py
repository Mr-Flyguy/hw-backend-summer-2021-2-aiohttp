from __future__ import annotations

from marshmallow import Schema, fields, validate


class ThemeCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1))


class ThemeSchema(Schema):
    id = fields.Int(required=True)
    title = fields.String(required=True)


class ThemeListSchema(Schema):
    themes = fields.List(fields.Nested(ThemeSchema), required=True)


class AnswerSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1))
    is_correct = fields.Bool(required=True)


class QuestionCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1))
    theme_id = fields.Int(required=True)
    answers = fields.List(fields.Nested(AnswerSchema), required=True, validate=validate.Length(min=1))


class QuestionSchema(Schema):
    id = fields.Int(required=True)
    title = fields.String(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.List(fields.Nested(AnswerSchema), required=True)


class QuestionListSchema(Schema):
    questions = fields.List(fields.Nested(QuestionSchema), required=True)
