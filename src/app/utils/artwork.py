from src.app.models import Artwork, Comment
from typing import Union
from flask import abort
from src.app import db


def get_object_or_404(
    object_type: str, object_id: int
) -> Union[Artwork, Comment]:
    """
    Get an artwork or comment by its ID or raise a 404 error if not found.
    """
    object_type = object_type.lower()
    if object_type == 'artwork':
        artwork = db.session.get(Artwork, object_id)
        if not artwork:
            print(f"Artwork with id {object_id} not found")
            abort(404, description=f"Artwork with id {object_id} not found")
        return artwork
    elif object_type == 'comment':
        comment = db.session.get(Comment, object_id)
        if not comment:
            print(f"Comment with id {object_id} not found")
            abort(404, description=f"Comment with id {object_id} not found")
        return comment
    else:
        abort(400, description="Invalid object type")
