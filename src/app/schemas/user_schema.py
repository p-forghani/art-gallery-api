from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(load_only=True)
    confirm_password = fields.Str(
        load_only=True,
        validate=validate.Equal("password", error="Passwords do not match")
    )


class ResetPasswordSchema(Schema):
    token = fields.String(required=True)
    new_password = fields.String(
        required=True, validate=validate.Length(min=8))
