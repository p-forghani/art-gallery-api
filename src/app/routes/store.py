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
from flask_restx import Resource, fields

# Define base models
error_model = store_ns.model('Error', {
    'status': fields.String(description='Status of the response'),
    'message': fields.String(description='Error message')
})

success_model = store_ns.model('Success', {
    'status': fields.String(description='Status of the response'),
    'message': fields.String(description='Success message')
})

# Define Artwork models
artwork_model = store_ns.model('Artwork', {
    'id': fields.Integer(description='Artwork ID'),
    'title': fields.String(description='Artwork title'),
    'description': fields.String(description='Artwork description'),
    'image_url': fields.String(description='URL of the artwork image'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp'),
    'user_id': fields.Integer(description='ID of the user who created the artwork')
})

# Define Comment models
comment_model = store_ns.model('Comment', {
    'id': fields.Integer(description='Comment ID'),
    'content': fields.String(description='Comment content'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp'),
    'user_id': fields.Integer(description='ID of the user who created the comment'),
    'artwork_id': fields.Integer(description='ID of the artwork this comment belongs to'),
    'parent_id': fields.Integer(description='ID of the parent comment if this is a reply')
})

# Define response models
artwork_list_response = store_ns.model('ArtworkListResponse', {
    'status': fields.String(description='Status of the response'),
    'data': fields.List(fields.Nested(artwork_model))
})

artwork_response = store_ns.model('ArtworkResponse', {
    'status': fields.String(description='Status of the response'),
    'data': fields.Nested(artwork_model)
})

upvote_response = store_ns.model('UpvoteResponse', {
    'status': fields.String(description='Status of the response'),
    'data': fields.Nested(store_ns.model('UpvoteData', {
        'upvotes': fields.Integer(description='Number of upvotes')
    }))
})

comment_list_response = store_ns.model('CommentListResponse', {
    'status': fields.String(description='Status of the response'),
    'data': fields.List(fields.Nested(comment_model))
})

comment_response = store_ns.model('CommentResponse', {
    'status': fields.String(description='Status of the response'),
    'message': fields.String(description='Success message'),
    'comment_id': fields.Integer(description='ID of the created comment')
})

@store_ns.route('/artworks', methods=['GET'])
class GetAllArtResource(Resource):
    @store_ns.doc('list_artworks',
        responses={
            200: ('Successfully retrieved all artworks', artwork_list_response),
            404: ('No artworks found', error_model),
            500: ('Internal server error', error_model)
        }
    )
    def get(self):
        """
        Get all artwork from the database.
        
        Returns:
            A list of all artwork with their details.
            If no artworks are found, returns a 404 error.
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
    @store_ns.doc('get_artwork',
        params={'artwork_id': 'The ID of the artwork to retrieve'},
        responses={
            200: ('Successfully retrieved artwork', artwork_response),
            400: ('Invalid input', error_model),
            404: ('Artwork not found', error_model)
        }
    )
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
        return {
            'status': 'success',
            'data': validated_data
        }, 200


@store_ns.route(
    '/upvote/<string:target_type>/<int:target_id>',
    methods=['GET', 'POST', 'DELETE'])
class UpvoteResource(Resource):
    @store_ns.doc('get_upvotes',
        params={
            'target_type': 'Type of the target (artwork or comment)',
            'target_id': 'ID of the target to get upvotes for'
        },
        responses={
            200: ('Successfully retrieved upvotes', upvote_response),
            400: ('Invalid target type', error_model),
            404: ('Target not found', error_model),
            500: ('Internal server error', error_model)
        }
    )
    def get(self, target_type, target_id):
        """
        Get the number of upvotes for an artwork or comment.
        
        Args:
            target_type (str): Type of the target ('artwork' or 'comment')
            target_id (int): ID of the target
            
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
    @store_ns.doc('upvote_target',
        params={
            'target_type': 'Type of the target (artwork or comment)',
            'target_id': 'ID of the target to upvote'
        },
        responses={
            200: ('Successfully upvoted', success_model),
            400: ('Invalid target type', error_model),
            401: ('Unauthorized', error_model),
            404: ('Target not found', error_model),
            500: ('Internal server error', error_model)
        },
        security='Bearer Auth'
    )
    def post(self, target_type, target_id):
        """
        Upvote an artwork or comment.
        
        Args:
            target_type (str): Type of the target ('artwork' or 'comment')
            target_id (int): ID of the target to upvote
            
        Returns:
            Success message if upvoted successfully
        """
        target = get_object_or_404(target_type, target_id)
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
    @store_ns.doc('remove_upvote',
        params={
            'target_type': 'Type of the target (artwork or comment)',
            'target_id': 'ID of the target to remove upvote from'
        },
        responses={
            200: ('Successfully removed upvote', success_model),
            400: ('Invalid target type', error_model),
            401: ('Unauthorized', error_model),
            404: ('Target not found', error_model),
            500: ('Internal server error', error_model)
        },
        security='Bearer Auth'
    )
    def delete(self, target_type, target_id):
        """
        Remove an upvote from an artwork or comment.
        
        Args:
            target_type (str): Type of the target ('artwork' or 'comment')
            target_id (int): ID of the target to remove upvote from
            
        Returns:
            Success message if upvote removed successfully
        """
        target = get_object_or_404(target_type, target_id)
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
    @store_ns.doc('add_comment',
        params={'artwork_id': 'The ID of the artwork to comment on'},
        body=store_ns.model('CommentInput', {
            'content': fields.String(required=True, description='Comment content')
        }),
        responses={
            201: ('Successfully added comment', comment_response),
            400: ('No data provided', error_model),
            401: ('Unauthorized', error_model),
            404: ('Artwork not found', error_model)
        },
        security='Bearer Auth'
    )
    def post(self, artwork_id):
        """
        Add a comment to an artwork.
        
        Args:
            artwork_id (int): The ID of the artwork to comment on
            
        Returns:
            A success message and the comment ID if the comment is added successfully
        """
        json_data = request.get_json()
        if not json_data or not json_data.get('content'):
            return {
                'status': 'error',
                'message': 'No data provided'
            }, 400
        artwork = get_object_or_404('artwork', artwork_id)
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

    @store_ns.doc('list_comments',
        params={'artwork_id': 'The ID of the artwork to get comments for'},
        responses={
            200: ('Successfully retrieved comments', comment_list_response),
            404: ('Artwork not found', error_model)
        }
    )
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
    @store_ns.doc('reply_to_comment',
        params={'comment_id': 'The ID of the comment to reply to'},
        body=store_ns.model('ReplyInput', {
            'content': fields.String(required=True, description='Reply content')
        }),
        responses={
            201: ('Successfully added reply', success_model),
            400: ('No data provided', error_model),
            401: ('Unauthorized', error_model),
            404: ('Comment not found', error_model)
        },
        security='Bearer Auth'
    )
    def post(self, comment_id):
        """
        Reply to a comment.
        
        Args:
            comment_id (int): The ID of the comment to reply to
            
        Returns:
            A success message if the reply is added successfully
        """
        json_data = request.get_json()
        if not json_data or not json_data.get('content'):
            return {
                'status': 'error',
                'message': 'No data provided'
            }, 400

        comment = get_object_or_404('comment', comment_id)
        assert isinstance(comment, Comment)
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
    @store_ns.doc('delete_comment',
        params={'comment_id': 'The ID of the comment to delete'},
        responses={
            200: ('Successfully deleted comment', success_model),
            401: ('Unauthorized', error_model),
            403: ('Forbidden - not the comment owner', error_model),
            404: ('Comment not found', error_model)
        },
        security='Bearer Auth'
    )
    def delete(self, comment_id):
        """
        Delete a comment.
        
        Args:
            comment_id (int): The ID of the comment to delete
            
        Returns:
            A success message if the comment is deleted successfully
        """
        comment = get_object_or_404('comment', comment_id)
        assert isinstance(comment, Comment)
        if comment.user_id != int(get_jwt_identity()):
            return {
                'message': 'You are not allowed to delete this comment.'
            }, 403
        db.session.delete(comment)
        db.session.commit()
        current_app.logger.info(
            f"Comment {comment_id} deleted successfully"
        )
        return {
            'status': 'success',
            'message': 'Comment deleted successfully'
        }, 200

    @store_ns.doc('list_replies',
        params={'comment_id': 'The ID of the comment to get replies for'},
        responses={
            200: ('Successfully retrieved replies', comment_list_response),
            404: ('Comment not found', error_model)
        }
    )
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
        comment_replies = (
            comment.replies
            .order_by(Comment.created_at.desc())
            .all()
        )
        schema = CommentOutputSchema(many=True)
        data = schema.dump(comment_replies)
        return {
            'status': 'success',
            'data': data
        }, 200
