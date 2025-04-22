from flask import jsonify
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
    try:
        artwork = Artwork.query.get(artwork_id)
        if artwork:
            return jsonify({
                'status': 'success',
                'data': artwork.to_dict()
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Artwork not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
