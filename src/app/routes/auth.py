from flask import current_app, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)

from src.app import db
from src.app.models import User
from src.app.routes import auth_bp
from src.app.schemas.user_schema import UserSchema


@auth_bp.route('/register', methods=['POST'])
def register():
    current_app.logger.info("Registering a new user")
    data = request.get_json()
    schema = UserSchema()
    # Validate the input data
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    # Check if the user already exists
    if User.query.filter_by(email=validated_data['email']).first():
        return jsonify({"message": "User already exists"}), 409

    new_user = User(
        name=validated_data['name'],
        email=validated_data['email'])
    new_user.set_password(validated_data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registered"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    current_app.logger.info("Logging in user")
    data = request.get_json()
    schema = UserSchema(only=('email', 'password'))
    # Validate the input data
    try:
        validate_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    # Check if the user exists and verify the password
    user = User.query.filter_by(email=validate_data['email']).first()
    if user and user.check_password(validate_data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.to_dict())
