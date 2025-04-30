from flask import abort, request, current_app
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_restx import Resource

from src.app import db
from src.app.models import Artwork, Category, Currency, Tag, User
from src.app.routes import artist_bp
from src.app.routes import artist_namespace as api
from src.app.schemas.art_schema import (ArtworkInputSchema,
                                        ArtworkOutputSchema, CategorySchema,
                                        CurrencySchema, TagSchema)


@artist_bp.before_request
def check_admin_access():
    current_app.logger.debug('Running check_admin_access()')
    verify_jwt_in_request()
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user or user.role_id != 2:
        return {"message": "Access forbidden: Artists only"}, 403


@api.route('/dashboard', methods=['GET'])
class ArtistDashboard(Resource):
    def get(self):
        current_app.logger.debug('Running ArtistDashboard.get()')
        # TODO: Paginate the artworks
        artworks = Artwork.query.filter_by(artist_id=get_jwt_identity()).all()
        schema = ArtworkOutputSchema(many=True)
        validated_artworks = schema.dump(artworks)
        return validated_artworks, 200


@api.route('/artwork/<int:artwork_id>', methods=['GET', 'PUT', 'DELETE'])
@api.route('/artwork', methods=['POST'])
class ArtworkResource(Resource):

    @staticmethod
    def get_artwork_or_404(artwork_id):
        """Helper method to get an artwork or return 404"""
        current_app.logger.debug('Running... get_artwork_or_404()')
        artwork = db.session.get(Artwork, int(artwork_id))
        if not artwork or artwork.artist_id != int(get_jwt_identity()):
            abort(404, description="Artwork not found")
        return artwork

    @staticmethod
    def add_artwork_tags(artwork, tag_names):
        """Helper method to handle artwork tags"""
        # Clear existing tags
        artwork.tags.clear()
        for tag_name in tag_names:
            # Check if tag exists
            tag = Tag.query.filter_by(title=tag_name.strip()).first()
            if not tag:
                # Create new tag if it doesn't exist
                tag = Tag(title=tag_name)
                db.session.add(tag)
                db.session.flush()
            artwork.tags.append(tag)

    @staticmethod
    def add_artwork_category(artwork, category_name):
        """Helper method to handle artwork category"""
        # Check if category exists
        category = Category.query.filter_by(
            title=category_name.strip()).first()
        if not category:
            # Create new category if it doesn't exist
            category = Category(title=category_name)
            db.session.add(category)
            db.session.flush()
        artwork.category_id = category.id

    def get(self, artwork_id):
        current_app.logger.debug('Running... ArtworkResource.get()')
        """Get a single artwork by ID"""
        # Check if the artwork exists and belongs to the current artist
        artwork = ArtworkResource.get_artwork_or_404(artwork_id)
        # Serialize the artwork
        schema = ArtworkOutputSchema()
        validated_artwork = schema.dump(artwork)
        return validated_artwork, 200

    def post(self):
        """Create a new artwork"""
        # Log the request data for debugging purposes
        current_app.logger.debug('Running... post()')
        data = request.get_json()
        schema = ArtworkInputSchema()
        try:
            validated_data = schema.load(data)
        except Exception as e:
            abort(
                400, description={"message": "Invalid input", "error": str(e)})

        tag_names = validated_data.pop('tag_names', [])
        category_name = validated_data.pop('category_name', None)
        # Create artwork without tags and category first
        new_artwork = Artwork(**validated_data)
        new_artwork.artist_id = get_jwt_identity()
        # Handle Category
        if category_name:
            ArtworkResource.add_artwork_category(new_artwork, category_name)
        # Handle new tags
        if tag_names:
            ArtworkResource.add_artwork_tags(new_artwork, tag_names)
        db.session.add(new_artwork)
        db.session.commit()
        return (
            {"message": "Artwork created", "artwork_id": new_artwork.id},
            201)

    def put(self, artwork_id):
        """
        Update an existing artwork by ID
        """

        # Check if the artwork exists and belongs to the current artist
        artwork = ArtworkResource.get_artwork_or_404(artwork_id)
        # Validate the request data
        data = request.get_json()
        schema = ArtworkInputSchema()
        validated_data = schema.load(data)

        tag_names = validated_data.pop('tag_names', [])

        # Update artwork fields
        for key, value in validated_data.items():
            setattr(artwork, key, value)

        category_name = validated_data.pop('category_name', None)
        # Handle Category
        if category_name:
            ArtworkResource.add_artwork_category(artwork, category_name)
        # Handle tags
        if tag_names:
            ArtworkResource.add_artwork_tags(artwork, tag_names)

        db.session.commit()
        return (
            {"message": "Artwork updated", "artwork_id": artwork.id}, 200)

    def delete(self, artwork_id):
        """
        Delete an existing artwork by ID
        """
        # Check if the artwork exists
        artwork = ArtworkResource.get_artwork_or_404(artwork_id)
        db.session.delete(artwork)
        db.session.commit()
        return (
            {"message": "Artwork deleted"}, 200)


@api.route('/tags', methods=['GET'])
class TagList(Resource):
    def get(self):
        """Get all tags"""
        tags = Tag.query.all()
        schema = TagSchema(many=True)
        validated_tags = schema.dump(tags)
        return validated_tags, 200


@api.route('/categories', methods=['GET'])
class CategoryList(Resource):
    def get(self):
        """Get all categories"""
        categories = Category.query.all()
        # Serialize the categories
        schema = CategorySchema(many=True)
        validated_categories = schema.dump(categories)
        # Return the serialized categories
        return validated_categories, 200


@api.route('/currencies', methods=['GET'])
class CurrencyList(Resource):
    def get(self):
        """Get all currencies"""
        currencies = Currency.query.all()
        schema = CurrencySchema(many=True)
        validated_currencies = schema.dump(currencies)
        return validated_currencies, 200
