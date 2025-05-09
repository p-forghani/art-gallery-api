from src.app import db
from datetime import timezone
from datetime import datetime


class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    currency_id = db.Column(
        db.Integer, db.ForeignKey('currency.id'), nullable=False)
    currency = db.relationship('Currency', back_populates='artworks')
    stock = db.Column(db.Integer, nullable=False)
    artist_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    artist = db.relationship('User', back_populates='artworks')
    # Path to the image file
    image_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime, default=datetime.now(tz=timezone.utc))
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='artworks')
    # TODO: Make the tags relationship lazy='dynamic' to avoid loading all tags
    # but carefull with other parts of the code that use it
    tags = db.relationship(
        'Tag', secondary='artwork_tags', back_populates='artworks')

    upvotes = db.relationship(
        'Upvote', back_populates='artwork', lazy='dynamic')
    comments = db.relationship(
        'Comment', back_populates='artwork', lazy='dynamic')

    def __repr__(self):
        return f"<Artwork {self.title}>"

    def is_upvoted(self, user_id):
        """
        Check if the artwork is upvoted by a specific user.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the artwork is upvoted by the user, False otherwise.
        """
        return Upvote.query.filter_by(
            user_id=user_id, artwork_id=self.id).count() > 0

    def upvote(self, user_id):
        """
        Upvote the artwork.

        Args:
            user_id (int): The ID of the user who upvoted the artwork.
        """
        if not self.is_upvoted(user_id):
            upvote = Upvote(user_id=user_id, artwork_id=self.id)
            db.session.add(upvote)
        else:
            raise ValueError("Artwork already upvoted by this user.")

    def remove_upvote(self, user_id) -> bool:
        """
        Remove an upvote from the artwork.

        Args:
            user_id (int): The ID of the user who upvoted the artwork.
        Returns:
            bool: True if the upvote was removed successfully, False otherwise.
        """
        upvote = Upvote.query.filter_by(
            user_id=user_id, artwork_id=self.id).first()
        if upvote:
            db.session.delete(upvote)
        else:
            raise ValueError("No upvote found for this user.")


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    artworks = db.relationship('Artwork', back_populates='category')

    def to_dict(self):
        """
        Convert the Category object to a dictionary representation.

        Returns:
            dict: A dictionary containing the category's details, including:
                - id (int): The ID of the category.
                - title (str): The title of the category.
        """
        return {
            'id': self.id,
            'title': self.title
        }

    def __repr__(self):
        return f"<Category {self.title}>"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    artworks = db.relationship(
        'Artwork', secondary='artwork_tags', back_populates='tags')

    def __repr__(self):
        return f"<Tag {self.title}>"


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    artworks = db.relationship('Artwork', back_populates='currency')

    def __repr__(self):
        return f"<Currency {self.title}>"


class Upvote(db.Model):
    __tablename__ = 'upvotes'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    artwork_id = db.Column(
        db.Integer, db.ForeignKey('artwork.id'), primary_key=True)
    created_at = db.Column(
        db.DateTime, default=datetime.now(tz=timezone.utc))

    user = db.relationship('User', back_populates='upvotes')
    artwork = db.relationship('Artwork', back_populates='upvotes')

    def __repr__(self):
        return (
            f"<Upvote user_id={self.user_id} "
            f"artwork_id={self.artwork_id} "
            f"created_at={self.created_at}>"
        )


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(
        db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.now(tz=timezone.utc))

    user = db.relationship('User', back_populates='comments')
    artwork = db.relationship('Artwork', back_populates='comments')

    def __repr__(self):
        return (
            f"<Comment user_id={self.user_id} "
            f"artwork_id={self.artwork_id} "
            f"created_at={self.created_at}>"
        )


# Association table for Artwork and Tag
artwork_tags = db.Table(
    'artwork_tags',
    db.Column(
        'artwork_id', db.Integer, db.ForeignKey('artwork.id'),
        primary_key=True),
    db.Column(
        'tag_id', db.Integer, db.ForeignKey('tag.id'),
        primary_key=True)
)
