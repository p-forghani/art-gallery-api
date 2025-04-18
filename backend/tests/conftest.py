import pytest
from backend.app.models import User, Category

from backend.app import create_app, db
from backend.config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def artist_user(app):
    """
    Create a test artist user with role_id = 2 (artist).
    """
    with app.app_context():
        artist = User(
            name="Test Artist", email="artist@example.com", role_id=2)
        artist.set_password("password")
        db.session.add(artist)
        db.session.commit()
        queried_user = User.query.filter_by(email="artist@example.com").first()
        print(f"User role ID: {queried_user.role_id}")
        return artist.to_dict()


@pytest.fixture
def category(app):
    """
    Create a test category for artworks.
    """
    with app.app_context():
        category = Category(title="Painting")
        db.session.add(category)
        db.session.commit()
        return category.to_dict()


@pytest.fixture
def auth_headers(client, artist_user):
    """
    Log in the artist user and return the authorization headers.
    """
    response = client.post("/auth/login", json={
        "email": artist_user["email"],
        "password": "password"
    })
    access_token = response.get_json()["access_token"]
    print(f"Access token: {access_token}")  # Debugging line to check the token
    return {"Authorization": f"Bearer {access_token}"}
