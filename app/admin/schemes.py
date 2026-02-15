from __future__ import annotations

from marshmallow import Schema, fields


class AdminLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class AdminSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Email(required=True)
