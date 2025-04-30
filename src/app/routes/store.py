from marshmallow import ValidationError
from src.app.schemas.art_schema import ArtworkOutputSchema
from src.app.models import Artwork
from src.app.routes import store_namespace as api
from flask_restx import Resource


@api.route('/', methods=['GET'])
class GetAllArtResource(Resource):

    def get(self):
        """
        Get all artwork from the database.
        Returns a list of all artwork with their details.
        """
        try:
            artworks = Artwork.query.all()
            if not artworks:
                return {
                    'status': 'error',
                    'message': 'No artworks found'
                }, 404
            schema = ArtworkOutputSchema(many=True)
            validated_data = schema.dump(artworks)
            # TODO: Add pagination
            return {
                'status': 'success',
                'data': validated_data
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }, 500


@api.route('/<int:artwork_id>', methods=['GET'])
class GetArtworkResource(Resource):
    def get(self, artwork_id):
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
                validated_data = schema.dump(artwork)
            except ValidationError as err:
                return {
                    'status': 'error',
                    'message': 'Invalid input',
                    'error': str(err)
                }, 400
            # Return the validated data
            return {
                'status': 'success',
                'data': validated_data
            }, 200
        else:
            return {
                'status': 'error',
                'message': 'Artwork not found'
            }, 404

# TODO: Implement the add-to-cart, cart, checkout, payment endpoints
