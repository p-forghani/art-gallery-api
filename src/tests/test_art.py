from src.app.models import Artwork


def test_create_artwork(client, auth_headers):
    """
    Test the creation of an artwork by an artist.
    """
    data = {
        "title": "Sunset Painting",
        "price": 150.0,
        "currency_id": 1,  # Assuming a currency with ID 1 exists
        "stock": 10,
        "description": "A beautiful sunset painting.",
        "category_name": "Painting",
        "tag_names": ["nature", "sunset"]
    }

    response = client.post("/artist/artwork", json=data, headers=auth_headers)
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["message"] == "Artwork created"
    assert "artwork_id" in response_data

    # Verify the artwork is in the database
    artwork = Artwork.query.get(response_data["artwork_id"])
    assert artwork is not None
    assert artwork.title == data["title"]
    assert artwork.price == data["price"]
    assert artwork.stock == data["stock"]
    assert artwork.description == data["description"]
    assert artwork.category.title == data["category_name"]
    assert len(artwork.tags) == 2
    assert {tag.title for tag in artwork.tags} == set(data["tag_names"])


def test_get_artwork(client, auth_headers, create_artwork):
    """
    Test retrieving an artwork by ID.
    """
    # First create an artwork to retrieve
    data = {
        "title": "Sunset Painting",
        "price": 150.0,
        "currency_id": 1,
        "stock": 10,
        "description": "A beautiful sunset painting.",
        "category_name": "Painting",
        "tag_names": ["nature", "sunset"]
    }
    artwork_id = create_artwork(data=data)

    # Now retrieve the artwork
    response = client.get(
        f"/artist/artwork/{artwork_id}",
        headers=auth_headers)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["id"] == artwork_id
    assert response_data["title"] == data["title"]


def test_update_artwork(client, auth_headers, create_artwork):
    """
    Test updating an existing artwork by ID.
    """
    # First create an artwork to update
    data = {
        "title": "Sunset Painting",
        "price": 150.0,
        "currency_id": 1,
        "stock": 10,
        "description": "A beautiful sunset painting.",
        "category_name": "Painting",
        "tag_names": ["nature", "sunset"]
    }
    artwork_id = create_artwork(data=data)

    # Now update the artwork
    updated_data = {
        "title": "Updated Sunset Painting",
        "price": 200.0,
        "currency_id": 1,
        "stock": 5,
        "description": "An updated beautiful sunset painting.",
        "category_name": "Art",
        "tag_names": ["nature", "sunset", "art"]
    }
    response = client.put(
        f"/artist/artwork/{artwork_id}",
        json=updated_data,
        headers=auth_headers)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["message"] == "Artwork updated"

    # Verify the artwork is updated in the database
    artwork = Artwork.query.get(artwork_id)
    assert artwork.title == updated_data["title"]
    assert artwork.price == updated_data["price"]
    assert artwork.stock == updated_data["stock"]
    assert artwork.description == updated_data["description"]
    assert artwork.category.title == updated_data["category_name"]
    assert len(artwork.tags) == 3
    assert {t.title for t in artwork.tags} == set(updated_data["tag_names"])


def test_delete_artwork(client, auth_headers, create_artwork):
    """
    Test deleting an artwork by ID.
    """
    data = {
        "title": "Sunset Painting",
        "price": 150.0,
        "currency_id": 1,
        "stock": 10,
        "description": "A beautiful sunset painting.",
        "category_name": "Painting",
        "tag_names": ["nature", "sunset"]
    }
    artwork_id = create_artwork(data=data)

    # Now delete the artwork
    response = client.delete(
        f"/artist/artwork/{artwork_id}",
        headers=auth_headers)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["message"] == "Artwork deleted"

    # Verify the artwork is deleted from the database
    artwork = Artwork.query.get(artwork_id)
    assert artwork is None

# TODO: Test invalid json
