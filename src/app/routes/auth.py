from flask import current_app, request
from flask_restx import Resource
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token, get_jwt, get_jwt_identity, jwt_required
)

from src.app.utils.mail_sender import send_reset_password_email
from src.app import db, jwt
from src.app.models import User, TokenBlocklist
from src.app.routes import auth_namespace as api
from src.app.schemas.user_schema import UserSchema, ResetPasswordSchema


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    """Check if the token is in the blocklist."""
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@api.route('/register', methods=['POST'])
class RegisterUserResource(Resource):
    def post(self):
        current_app.logger.info("Registering a new user")
        schema = UserSchema()
        # Validate the input data
        try:
            validated_data = schema.load(request.get_json())  # type: ignore
        except ValidationError as err:
            return err.messages, 400
        # Check if the user already exists
        if User.query.filter_by(
            email=validated_data['email']  # type: ignore
        ).first():
            return {"message": "User already exists"}, 409

        new_user = User(
            name=validated_data['name'],  # type: ignore
            email=validated_data['email'])  # type: ignore
        new_user.set_password(validated_data['password'])  # type: ignore
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
            validate_data = schema.load(request.get_json())  # type: ignore
        except ValidationError as err:
            return err.messages, 400
        # Check if the user exists and verify the password
        user = User.query.filter_by(
            email=validate_data['email']  # type: ignore
        ).first()
        if user and user.check_password(
            validate_data['password']  # type: ignore
        ):
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


@api.route('/logout', methods=['POST'])
class LogoutUserResource(Resource):
    @jwt_required()
    def post(self):
        """Logout the current user by blacklisting their JWT token."""
        jti = get_jwt()["jti"]
        db.session.add(TokenBlocklist(jti=jti))  # type: ignore
        db.session.commit()
        return {"message": "Successfully logged out"}, 200


@api.route('/forgot-password', methods=['POST'])
class ForgotPasswordResource(Resource):
    def post(self):
        current_app.logger.info("Forgot password")
        schema = UserSchema(only=(['email']))
        # Validate the input data
        try:
            validated_data = schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        # Check if the user exists
        user = User.query.filter_by(
            email=validated_data['email']  # type: ignore
        ).first()
        if user:
            # Generate a reset token
            reset_token = user.generate_reset_token()
            # Send the reset email
            send_reset_password_email(user.email, reset_token)
            return {"message": "Reset Password Request Received Successfully"}


@api.route('/reset-password', methods=['PUT'])
class ResetPasswordResource(Resource):
    def put(self):
        current_app.logger.info("Reset password")
        # Validate the input data
        try:
            validated_data = ResetPasswordSchema().load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        # Fetch the user by ID
        user = db.session.get(
            User,
            User.verify_reset_token(
                token=validated_data['token']  # type: ignore
            )
        )
        if user is None:
            return {"message": "User not found"}, 404
        user.set_password(validated_data['new_password'])  # type: ignore
        db.session.commit()
        return {"message": "Password reset successfully"}, 200
