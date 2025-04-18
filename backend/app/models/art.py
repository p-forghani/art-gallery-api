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
    artist_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    artist = db.relationship('User', back_populates='artworks')
    # Path to the image file
    image_path = db.Column(db.String(255), nullable=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='artworks')
    tags = db.relationship(
        'Tag', secondary='artwork_tags', back_populates='artworks')

    def to_dict(self):
        """
        Convert the Artwork object to a dictionary representation.

        Returns:
            dict: A dictionary containing the artwork's details, including:
                - id (int): The ID of the artwork.
                - title (str): The title of the artwork.
                - price (float): The price of the artwork.
                - stock (int): The stock quantity of the artwork.
                - description (str): The description of the artwork.
                - category (dict): A dictionary containing the category
                details, including:
                    - id (int): The ID of the category.
                    - title (str): The title of the category.
                - tags (list): A list of tag titles associated with the
                artwork.
                - image_path (str): The path to the image file of the artwork.
                - currency (dict): A dictionary containing the currency
                details, including:
                    - id (int): The ID of the currency.
                    - title (str): The title of the currency.
                    - symbol (str): The symbol of the currency.
        """
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'stock': self.stock,
            'description': self.description,
            'category': {
                'id': self.category.id,
                'title': self.category.title
            },
            'tags': [tag.title for tag in self.tags],
            'image_path': self.image_path,
            'currency': {
                'id': self.currency.id,
                'title': self.currency.title,
                'symbol': self.currency.symbol
            }
        }

    def __repr__(self):
        return f"<Artwork {self.title}>"


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
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    artworks = db.relationship('Artwork', back_populates='currency')

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
