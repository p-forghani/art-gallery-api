from marshmallow import ValidationError
from src.app.schemas.store_schema import CommentOutputSchema
from src.app.models import Comment, Artwork
from flask import request
from src.app.utils.artwork import get_object_or_404
from flask import current_app
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from src.app import db
from src.app.schemas.art_schema import ArtworkOutputSchema
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
        artwork = get_object_or_404('artwork', artwork_id)
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


@store_ns.route(
    '/upvote/<string:target_type>/<int:target_id>',
    methods=['GET', 'POST', 'DELETE'])
class UpvoteResource(Resource):
    def get(self, target_type, target_id):
        """
        Get the number of upvotes for an artwork or comment.
        Returns:
            The number of upvotes for the artwork or comment
        """

        if target_type not in ['artwork', 'comment']:
            return {
                'status': 'error',
                'message': 'Invalid target type'
            }, 400
        target = get_object_or_404(target_type, target_id)
        try:
            upvotes_count = target.get_upvotes_count()
            return {
                'status': 'success',
                'data': {
                    'upvotes': upvotes_count
                }
            }, 200
        except Exception as e:
            current_app.logger.error(f"Error getting upvotes count: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }, 500

    @jwt_required()
    def post(self, target_type, target_id):
        """
        Upvote an artwork or comment by its ID.
        """
        print('Calling UpvoteResource.post()...')  # DEBUGGING
        target = get_object_or_404(target_type, target_id)
        #  Get the current user ID from the JWT token
        current_user_id = get_jwt_identity()
        try:
            target.upvote(current_user_id)
            db.session.commit()
            return {
                'status': 'success',
                'message': f'{target_type.capitalize()} upvoted successfully'
            }, 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error upvoting {target_type}: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }, 500

    @jwt_required()
    def delete(self, target_type, target_id):
        """
        Remove an upvote from an artwork or comment by its ID.
        """
        target = get_object_or_404(target_type, target_id)
        #  Get the current user ID from the JWT token
        current_user_id = get_jwt_identity()
        try:
            target.remove_upvote(current_user_id)
            db.session.commit()
            return {
                'status': 'success',
                'message': f'Upvote removed successfully from {target_type}'
            }, 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error removing upvote: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }, 400


@store_ns.route(
    '/artworks/<int:artwork_id>/comments',
    methods=['POST', 'GET'])
class CommentArtworkResource(Resource):
    @jwt_required()
    def post(self, artwork_id):
        """
        Add a comment to an artwork.
        Args:
            artwork_id (int): The ID of the artwork to comment on
        Returns:
            A success message if the comment is added successfully, or an error
            message if not
        """
        json_data = request.get_json()
        if not json_data or not json_data.get('content'):
            return {
                'status': 'error',
                'message': 'No data provided'
            }, 400
        artwork = get_object_or_404('artwork', artwork_id)
        # This line ensures that the artwork is an instance of Artwork
        assert isinstance(artwork, Artwork)
        comment_id = artwork.add_comment(
            user_id=get_jwt_identity(),
            content=json_data.get('content'),
        )
        db.session.commit()

        current_app.logger.info(
            f"Comment added successfully to artwork {artwork_id}"
        )
        return {
            'status': 'success',
            'message': 'Comment added successfully',
            'comment_id': comment_id,
        }, 201

    def get(self, artwork_id):
        """
        List comments for an artwork.
        Args:
            artwork_id (int): The ID of the artwork to get comments for
        Returns:
            A list of comments for the artwork
        """
        artwork = get_object_or_404('artwork', artwork_id)
        assert isinstance(artwork, Artwork)
        comments = (
            artwork.comments
            .filter_by(parent_id=None)
            .order_by(Comment.created_at.desc())
            .all())
        schema = CommentOutputSchema(many=True)
        data = schema.dump(comments)
        return {
            'status': 'success',
            'data': data
        }, 200


@store_ns.route(
    "/comments/<int:comment_id>",
    methods=["POST", "DELETE", "GET"]
)
class CommentResource(Resource):
    @jwt_required()
    def post(self, comment_id):
        """
        Reply to a comment.
        """
        json_data = request.get_json()
        if not json_data or not json_data.get('content'):
            return {
                'status': 'error',
                'message': 'No data provided'
            }, 400

        comment = get_object_or_404('comment', comment_id)
        assert isinstance(comment, Comment)
        # Add the reply to the comment
        comment.add_reply(
            user_id=get_jwt_identity(),
            content=json_data.get('content'),
        )
        db.session.commit()
        current_app.logger.info(
            f"Reply added successfully to comment {comment_id}"
        )
        return {
            'status': 'success',
            'message': 'Reply added successfully'
        }, 201

    @jwt_required()
    def delete(self, comment_id):
        """
        Delete a comment
        """
        comment = get_object_or_404('comment', comment_id)
        assert isinstance(comment, Comment)
        db.session.delete(comment)
        db.session.commit()
        current_app.logger.info(
            f"Comment {comment_id} deleted successfully"
        )
        return {
            'status': 'success',
            'message': 'Comment deleted successfully'
        }, 200

    def get(self, comment_id):
        """
        List replies for a comment.
        Args:
            comment_id (int): The ID of the comment to get replies for
        Returns:
            A list of replies for the comment
        """
        comment = get_object_or_404('comment', comment_id)
        assert isinstance(comment, Comment)
        # DEBUGGING: Check out what is the problem with this code
        # TODO: paginate this
        comment_replies = (
            comment.replies  # type: ignore
            .order_by(Comment.created_at.desc())
            .all()
        )
        schema = CommentOutputSchema(many=True)
        data = schema.dump(comment_replies)
        return {
            'status': 'success',
            'data': data
        }, 200
