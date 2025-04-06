from backend.app.routes import admin_bp
from backend.app.models.art import Category
from backend.app.models.art import Tag
from backend.app import db
from backend.app.models.user import User
from backend.app.models.art import Artwork
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


@admin_bp.before_request
@jwt_required()
def check_admin_access():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role_id != 2:
        return jsonify(
            {"message": "Access forbidden: Admins only"}), 403


# Create a new artwork
@admin_bp.route('/', methods=['POST'])
def create_artwork():
    data = request.get_json()

    # Handle category: accept either category_id or category_title
    category_id = data.get('category_id')
    if not category_id:
        category_title = data.get('category_title')
        if not category_title:
            return jsonify(
                {"message": "Category ID or title is required"}), 400

    # Resolve category_id from category_title
    category = Category.query.filter_by(title=category_title).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404
    category_id = category.id

    # Handle tags
    tag_names = data.get('tags', [])
    tags = []
    for tag_name in tag_names:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        tags.append(tag)

    new_artwork = Artwork(
        name=data.get('title'),
        description=data.get('description'),
        category_id=category_id,
        tags=tags
    )

    db.session.add(new_artwork)
    db.session.commit()
    return jsonify(
        {"message": "Artwork created", "artwork": new_artwork.id}), 201


# Read all artworks
@admin_bp.route('/', methods=['GET'])
def get_all_artworks():
    # TODO
    pass


# Read a single artwork by ID
@admin_bp.route('/<int:artwork_id>', methods=['GET'])
def get_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    return jsonify(artwork.to_dict()), 200


# Update an artwork by ID
@admin_bp.route('/<int:artwork_id>', methods=['PUT'])
def update_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    data = request.get_json()
    artwork.title = data.get('title', artwork.title)
    artwork.description = data.get('description', artwork.description)

    # Handle category: accept either category_id or category_title
    category_id = data.get('category_id')
    if not category_id:
        category_title = data.get('category_title')
        if not category_title:
            return jsonify(
                {"message": "Category ID or title is required"}), 400

    # Resolve category_id from category_title
    category = Category.query.filter_by(title=category_title).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404
    category_id = category.id

    # Handle tags
    tag_names = data.get('tags', [])
    if tag_names:
        tags = []
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            tags.append(tag)
        artwork.tags = tags

    db.session.commit()
    return jsonify({"message": "Artwork updated"}), 200


# Delete an artwork by ID
@admin_bp.route('/<int:artwork_id>', methods=['DELETE'])
def delete_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    db.session.delete(artwork)
    db.session.commit()
    return jsonify({"message": "Artwork deleted"}), 200
