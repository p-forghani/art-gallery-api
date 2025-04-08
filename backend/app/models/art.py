from backend.app import db


class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    currency_id = db.Column(
        db.Integer, db.ForeignKey('currency.id'), nullable=False)
    currency = db.relationship('Currency', back_populates='artworks')
    stock = db.Column(db.Integer, nullable=False)
    # Path to the image file
    image_path = db.Column(db.String(255), nullable=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='artworks')
    tags = db.relationship(
        'Tag', secondary='artwork_tags', back_populates='artworks')

    def to_dict(self):
        """
        Convert the Artwork instance to a dictionary representation.

        Returns:
            dict: A dictionary containing the artwork details:
                - id (int): The unique identifier of the artwork.
                - title (str): The title of the artwork.
                - price (float): The price of the artwork.
                - stock (int): The stock quantity of the artwork.
                - description (str): The description of the artwork.
                - category (str): The title of the category the artwork
                belongs to.
                - tags (list): A list of tag names associated with the artwork.
                - image_path (str): The path to the image file of the artwork.
        """
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "stock": self.stock,
            "description": self.description,
            "category": self.category.title,
            "tags": [tag.name for tag in self.tags],
            "image_path": self.image_path
        }

    def __repr__(self):
        return f"<Artwork {self.title}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    artworks = db.relationship('Artwork', back_populates='category')

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
    symbol = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f"<Currency {self.title}>"


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
