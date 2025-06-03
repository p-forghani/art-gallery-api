from src.app import db
from datetime import timezone
from datetime import datetime


# TODO: Integrate UpvotableMixin approach to the previous upvote system

class UpvotableMixin:
    """
    Mixin class to add upvote functionality to models.
    This mixin provides methods to check if an item is upvoted,
    upvote an item, and remove an upvote.
    """
    def is_upvoted(self, user_id):
        return Upvote.query.filter_by(
            user_id=user_id,
            target_type=self.__class__.__name__.lower(),
            # Using getattr instead of self.id to avoid AttributeError
            target_id=getattr(self, 'id', None)
        ).count() > 0

    def upvote(self, user_id):
        if not self.is_upvoted(user_id):
            upvote = Upvote(
                user_id=user_id,  # type: ignore
                target_type=self.__class__.__name__.lower(),  # type: ignore
                target_id=getattr(self, 'id', None)  # type: ignore
            )
            db.session.add(upvote)
        else:
            raise ValueError(
                f"{self.__class__.__name__} already upvoted by this user.")

    def remove_upvote(self, user_id):
        upvote = Upvote.query.filter_by(
            user_id=user_id,
            target_type=self.__class__.__name__.lower(),
            target_id=getattr(self, 'id', None)
        ).first()
        if upvote:
            db.session.delete(upvote)
        else:
            raise ValueError("No upvote found for this user.")

    def get_upvotes_count(self) -> int:
        return Upvote.query.filter_by(
            target_type=self.__class__.__name__.lower(),
            target_id=self.id).count()  # type: ignore

    def get_upvotes(self):
        return Upvote.query.filter_by(
            target_type=self.__class__.__name__.lower(),
            target_id=self.id).all()  # type: ignore


class Artwork(db.Model, UpvotableMixin):
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
        'Tag', secondary='artwork_tags', back_populates='artworks',
        cascade="save-update, merge")

    comments = db.relationship(
        'Comment', back_populates='artwork', lazy='dynamic',
        cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Artwork {self.title}>"

    def add_comment(self, user_id, content):
        """
        Add a comment to the artwork.

        Args:
            user_id (int): The ID of the user who commented.
            content (str): The content of the comment.
        """
        comment = Comment(
            user_id=user_id,  # type: ignore
            artwork_id=self.id,  # type: ignore
            content=content  # type: ignore
        )
        db.session.add(comment)
        db.session.flush()
        return comment.id

    def remove_comment(self, comment_id):
        # TODO: Implement this method to remove a comment by its ID
        pass


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
    __tablename__ = 'upvote'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(
        db.DateTime, default=datetime.now(tz=timezone.utc))
    target_type = db.Column(db.String(20), primary_key=True)
    target_id = db.Column(db.Integer, primary_key=True)

    user = db.relationship('User', back_populates='upvotes')

    __table_args__ = (
        db.UniqueConstraint(
            'user_id', 'target_type', 'target_id', name='unique_upvote'),
    )


class Comment(db.Model, UpvotableMixin):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.now(tz=timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artwork_id = db.Column(
        db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    user = db.relationship('User', back_populates='comments')
    artwork = db.relationship('Artwork', back_populates='comments')

    # Make Comment self-refrential
    parent_id = db.Column(
        db.Integer, db.ForeignKey('comment.id'), nullable=True, default=None
    )
    parent = db.relationship(
        'Comment',
        remote_side=[id],
        back_populates='replies',
        lazy='joined'
    )

    replies = db.relationship(
        'Comment',
        back_populates='parent',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return (
            f"<Comment user_id={self.user_id} "
            f"artwork_id={self.artwork_id} "
            f"created_at={self.created_at}>"
        )

    def add_reply(self, user_id, content):
        """
        Add a reply to the comment.

        Args:
            user_id (int): The ID of the user who replied.
            content (str): The content of the reply.
        """
        reply = Comment(
            user_id=user_id,  # type: ignore
            artwork_id=self.artwork_id,  # type: ignore
            content=content,  # type: ignore
            parent_id=self.id  # type: ignore
        )
        db.session.add(reply)


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
