from flask import current_app, request
from flask_restx import Resource
from marshmallow import ValidationError
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)

from src.app import db
from src.app.models import User
from src.app.routes import auth_namespace as api
from src.app.schemas.user_schema import UserSchema


@api.route('/register', methods=['POST'])
class RegisterUserResource(Resource):
    def post(self):

        current_app.logger.info("Registering a new user")
        schema = UserSchema()
        # Validate the input data
        try:
            validated_data = schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        # Check if the user already exists
        if User.query.filter_by(email=validated_data['email']).first():
            return {"message": "User already exists"}, 409

        new_user = User(
            name=validated_data['name'],
            email=validated_data['email'])
        new_user.set_password(validated_data['password'])
        db.session.add(new_user)
        db.session.commit()

        return {"message": "Registered", "user": schema.dump(new_user)}, 201


@api.route('/login', methods=['POST'])
class LoginUserResource(Resource):

    def post(self):
        current_app.logger.info("Logging in user")
        schema = UserSchema(only=('id', 'email', 'password'))
        # Validate the input data
        try:
            validate_data = schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        # Check if the user exists and verify the password
        user = User.query.filter_by(email=validate_data['email']).first()
        if user and user.check_password(validate_data['password']):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401


@api.route('/profile', methods=['GET'])
class UserProfileResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if user is None:
            return {"message": "User not found"}, 404
        schema = UserSchema()
        return schema.dump(user), 200
