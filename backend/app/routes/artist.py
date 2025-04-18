from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.app import db
from backend.app.models import Artwork, Category, Tag
from backend.app.schemas.art_schema import (
    ArtworkInputSchema, ArtworkOutputSchema)
from backend.app.models import User
from backend.app.routes import artist_bp


@artist_bp.before_request
@jwt_required()
def check_admin_access():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role_id != 2:
        return jsonify(
            {"message": "Access forbidden: Artists only"}), 403


# Create a new artwork
@artist_bp.route('/', methods=['GET', 'POST'])
def create_artwork():

    # DEBUGGING
    print(f"request.method: {request.method}")
    print(f"request.json: {request.json}")

    if request.method == 'GET':
        # Return data needed to populate the form
        categories = Category.query.all()
        tags = Tag.query.all()
        return jsonify({
            "categories": [{"id": c.id, "name": c.name} for c in categories],
            "tags": [{"id": t.id, "name": t.name} for t in tags]
        }), 200

    # POST method - create new artwork
    data = request.get_json()
    schema = ArtworkInputSchema()
    # Client will send category_id
    validated_data = schema.validate(data)

    tag_names = validated_data.pop('tag_names', [])

    # Create artwork without tags first
    new_artwork = Artwork(**validated_data)
    db.session.add(new_artwork)

    # Handle new tags
    if tag_names:
        for tag_name in tag_names:
            # Check if tag exists
            tag = Tag.query.filter_by(name=tag_name.strip()).first()
            if not tag:
                # Create new tag if it doesn't exist
                tag = Tag(name=tag_name)
                db.session.add(tag)
            new_artwork.tags.append(tag)

    db.session.commit()
    return jsonify(
        {"message": "Artwork created", "artwork_id": new_artwork.id}), 201


# Read a single artwork by ID
@artist_bp.route('/<int:artwork_id>', methods=['GET'])
def get_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(ident=artwork_id)
    return jsonify(artwork.to_dict()), 200


# Update an artwork by ID
@artist_bp.route('/<int:artwork_id>', methods=['GET', 'PUT'])
def update_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)

    if request.method == 'GET':
        # Return data needed to populate the form
        schema = ArtworkOutputSchema()
        # Client needs categories and tags to populate the form
        categories = Category.query.all()
        tags = Tag.query.all()
        return jsonify({
            "artwork": schema.dump(artwork),
            "categories": [{"id": c.id, "title": c.title} for c in categories],
            "tags": [{"id": t.id, "title": t.title} for t in tags]
        }), 200

    # PUT method - update existing artwork
    data = request.get_json()
    schema = ArtworkInputSchema()
    validated_data = schema.validate(data)

    tag_names = validated_data.pop('tag_names', [])

    # Update artwork fields
    for key, value in validated_data.items():
        setattr(artwork, key, value)

    # Handle tags
    if tag_names:
        # Clear existing tags
        artwork.tags.clear()
        for tag_name in tag_names:
            # Check if tag exists
            tag = Tag.query.filter_by(name=tag_name.strip()).first()
            if not tag:
                # Create new tag if it doesn't exist
                tag = Tag(name=tag_name)
                db.session.add(tag)
            artwork.tags.append(tag)

    db.session.commit()
    return jsonify({"message": "Artwork updated",
                    "artwork_id": artwork.id}), 200


# Delete an artwork by ID
@artist_bp.route('/<int:artwork_id>', methods=['DELETE'])
def delete_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    db.session.delete(artwork)
    db.session.commit()
    return jsonify({"message": "Artwork deleted"}), 200
