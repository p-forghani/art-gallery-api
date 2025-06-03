from marshmallow import Schema
from marshmallow import fields


class CommentOutputSchema(Schema):
    id = fields.Int()
    content = fields.Str()
    created_at = fields.DateTime()
    user_id = fields.Int()
    upvotes = fields.Method('get_upvotes_count')
    # For nested replies (recursive)
    replies = fields.Nested(lambda: CommentOutputSchema(), many=True)

    def get_upvotes_count(self, obj):
        return (
            obj.get_upvotes_count()
            if hasattr(obj, "get_upvotes_count")
            else 0
        )

