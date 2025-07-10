from datetime import datetime, timezone
import os
import jwt as pyjwt
from src.app import jwt
from src.app import db
from src.app import bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(
        db.Integer, db.ForeignKey('role.id'), nullable=False, default=3)
    role = db.relationship('Role', back_populates='users')
    password_hash = db.Column(db.String(128), nullable=False)
    artworks = db.relationship('Artwork', back_populates='artist')
    upvotes = db.relationship('Upvote', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')

    def __repr__(self):
        return f"<User {self.name}>"

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_reset_token(self) -> str:
        return pyjwt.encode(
            payload={'reset_password': str(self.id)},
            key=os.getenv('SECRET_KEY'),
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_token(token: str):
        """
        Verify the reset token and return the user id if valid.

        :param token: The JWT token to verify.
        :return: user id if the token is valid, None otherwise.
        """
        try:
            payload = pyjwt.decode(
                token,
                key=os.getenv('SECRET_KEY'),
                algorithms=['HS256']
            )
            user_id = payload.get('reset_password')
            return user_id
        except (pyjwt.ExpiredSignatureError, pyjwt.InvalidTokenError):
            return None

    def to_dict(self):
        """
        Convert the User object to a dictionary.
        This is useful for serializing the object to JSON.

        :return: A dictionary representation of the User object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role_id": self.role_id
        }


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', back_populates='role')

    def __repr__(self):
        return f"<Role {self.name}>"


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc))
