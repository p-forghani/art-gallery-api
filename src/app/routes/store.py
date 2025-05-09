from marshmallow import ValidationError
from flask import current_app
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.app import db
from src.app.schemas.art_schema import ArtworkOutputSchema
from src.app.models import Artwork
from src.app.routes import store_namespace as store_ns
from flask_restx import Resource


@store_ns.route('/artworks', methods=['GET'])
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


@store_ns.route('/artworks/<int:artwork_id>', methods=['GET'])
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


@store_ns.route(
    '/artworks/<int:artwork_id>/upvote',
    methods=['POST', 'DELETE'])
class UpvoteArtworkResource(Resource):
    @jwt_required()
    def post(self, artwork_id):
        """
        Upvote an artwork by its ID.
        Args:
            artwork_id (int): The ID of the artwork to upvote
        Returns:
            A success message if the upvote is successful, or an error message
            if not
        """
        artwork = db.session.get(Artwork, artwork_id)
        if not artwork:
            return {
                'status': 'error',
                'message': 'Artwork not found'
            }, 404
        #  Get the current user ID from the JWT token
        current_user_id = get_jwt_identity()
        try:
            artwork.upvote(current_user_id)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Artwork upvoted successfully'
            }, 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error upvoting artwork: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }, 500

    @jwt_required()
    def delete(self, artwork_id):
        """
        Remove an upvote from an artwork by its ID.
        Args:
            artwork_id (int): The ID of the artwork to remove the upvote from
        Returns:
            A success message if the upvote removal is successful, or an error
            message if not
        """
        artwork = db.session.get(Artwork, artwork_id)
        if not artwork:
            return {
                'status': 'error',
                'message': 'Artwork not found'
            }, 404
        #  Get the current user ID from the JWT token
        current_user_id = get_jwt_identity()
        try:
            artwork.remove_upvote(current_user_id)
            db.session.commit()
            return {
                'status': 'success',
                'message': 'Upvote removed successfully'
            }, 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error removing upvote: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }, 400


@store_ns.route(
    '/artworks/<int:artwork_id>/upvotes',
    methods=['GET'])
class UpvotesCountResource(Resource):
    def get(self, artwork_id):
        """
        Get the number of upvotes for an artwork.
        Returns:
            The number of upvotes for the artwork
        """
        artwork = db.session.get(Artwork, artwork_id)
        if not artwork:
            return {
                'status': 'error',
                'message': 'Artwork not found'
            }, 404
        try:
            upvotes_count = artwork.upvotes.count()
            return {
                'status': 'success',
                'data': {
                    'upvotes': upvotes_count
                }
            }, 200
        except Exception as e:
            print(f"Error getting upvotes count: {str(e)}")  # DEBUGGING
            return {
                'status': 'error',
                'message': str(e)
            }, 500
