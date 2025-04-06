from backend.app import db


class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='artworks')
    tags = db.relationship(
        'Tag', secondary='artwork_tags', back_populates='artworks')

    # TODO: Link artwork picture to instance

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category.title,
            "tags": [tag.name for tag in self.tags]
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    artworks = db.relationship('Artwork', back_populates='category')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    artworks = db.relationship(
        'Artwork', secondary='artwork_tags', back_populates='tags')


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
