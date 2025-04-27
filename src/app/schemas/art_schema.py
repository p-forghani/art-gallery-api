from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError


# The formats for the Artwork schema that the client will send
class ArtworkInputSchema(Schema):
    title = fields.Str(required=True)
    price = fields.Float(required=True)
    currency_id = fields.Int(required=True)
    stock = fields.Int(required=True)
    description = fields.Str(required=True)
    category_name = fields.Str(required=True)
    tag_names = fields.List(fields.Str(), required=False)
    image_path = fields.Str(required=False)


# The formats for the Artwork schema that the client will receive
class ArtworkOutputSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    price = fields.Float(required=True)
    stock = fields.Int(required=True)
    description = fields.Str(required=True)
    category = fields.Nested('CategorySchema', required=True)
    tags = fields.List(fields.Str(), required=True)
    image_path = fields.Str(required=False)
    currency = fields.Nested('CurrencySchema', required=True)


class CurrencySchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    symbol = fields.Str(required=True)


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)

    def validate_title(self, value):
        if not value:
            raise ValidationError("Title cannot be empty.")


class TagSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
