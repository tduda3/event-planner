# app/schemas.py
from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)

class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    datetime = fields.DateTime(required=True)
    location = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    owner_id = fields.Int(dump_only=True)

class RegistrationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    event_id = fields.Int(required=True)
    timestamp = fields.DateTime(dump_only=True)