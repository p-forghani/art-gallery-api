import pytest
from src.app.models import User

from src.app import create_app, db
from src.config import TestingConfig
from src.app.schemas.user_schema import UserSchema


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
            name="Test Artist",  # type: ignore
            email="artist@example.com",  # type: ignore
            role_id=2  # type: ignore
        )
        artist.set_password("password")
        db.session.add(artist)
        db.session.commit()
        queried_user = User.query.filter_by(email="artist@example.com").first()
        assert queried_user is not None, (
            "Artist user was not created successfully."
        )
        assert queried_user.role_id == 2, (
            "Artist user does not have the correct role_id."
        )
        assert queried_user.check_password("password"), (
            "Artist user password is incorrect."
        )
        return UserSchema().dump(artist)


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
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def create_artwork(client, auth_headers):
    """
    Helper function to create an artwork.
    """
    def _create_artwork(data=None):
        if data is None:
            data = {
                "title": "Default Artwork",
                "price": 100.0,
                "currency_id": 1,  # Assuming a currency with ID 1 exists
                "stock": 5,
                "description": "Default description.",
                "category_name": "Default Category",
                "tag_names": ["default", "tag"]
            }
        response = client.post(
            "/artist/artwork", json=data, headers=auth_headers)
        assert response.status_code == 201
        return response.get_json()["artwork_id"]
    return _create_artwork


@pytest.fixture
def general_auth_headers(app, client):
    with app.app_context():
        user = User(
            name="General User",  # type: ignore
            email="general@example.com",  # type: ignore
            role_id=3  # type: ignore
        )
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        queried_user = User.query.filter_by(
            email="general@example.com"
        ).first()
        assert queried_user is not None, (
            "General user was not created successfully."
        )
        assert queried_user.check_password("password"), (
            "General user password is incorrect."
        )
    response = client.post("/auth/login", json={
        "email": "general@example.com",
        "password": "password"
    })
    access_token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def comment_artwork(create_artwork, client):
    artwork_id = create_artwork()
    r = client.post(
        f"/store/artworks/{artwork_id}/comments",
        json={'content': 'Great'},
        headers=general_auth_headers
    )
    comment_id = r.get_json()['data']['comment_id']
    return comment_id
