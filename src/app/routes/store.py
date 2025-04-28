from flask import jsonify
from flask import abort
from marshmallow import ValidationError
from src.app.schemas.art_schema import ArtworkOutputSchema
from src.app.models import Artwork
from src.app.routes import store_bp


@store_bp.route('/', methods=['GET'])
def get_all_art():
    """
    Get all artwork from the database.
    Returns a list of all artwork with their details.
    """
    try:
        artworks = Artwork.query.all()
        # TODO: Add pagination
        return jsonify({
            'status': 'success',
            'data': [artwork.to_dict() for artwork in artworks]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@store_bp.route('/<int:artwork_id>', methods=['GET'])
def get_artwork(artwork_id):
    """
    Get a single artwork by its ID.
    Args:
        artwork_id (int): The ID of the artwork to retrieve
    Returns:
        The artwork details if found, or an error message if not found
    """
    artwork = Artwork.query.get(artwork_id)
    if artwork:
        schema = ArtworkOutputSchema()
        try:
            validated_data = schema.load(artwork.to_dict())
        except ValidationError as err:
            return abort(
                400,
                description={"message": "Invalid input", "error": str(err)})
        # Return the validated data
        return jsonify({
            'status': 'success',
            'data': validated_data
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Artwork not found'
        }), 404

# TODO: Implement the add-to-cart, cart, checkout, payment endpoints
