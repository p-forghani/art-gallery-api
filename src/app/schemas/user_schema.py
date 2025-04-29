from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(load_only=True)
    confirm_password = fields.Str(load_only=True)

    def validate_passwords(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError("Passwords do not match")
        return data

