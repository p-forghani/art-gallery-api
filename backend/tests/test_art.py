from backend.app.models import Artwork


def test_create_artwork(client, auth_headers, category):
    """
    Test the creation of an artwork by an artist.
    """
    data = {
        "title": "Sunset Painting",
        "price": 150.0,
        "currency_id": 1,  # Assuming a currency with ID 1 exists
        "stock": 10,
        "description": "A beautiful sunset painting.",
        "category_id": category["id"],
        "tag_names": ["nature", "sunset"]
    }

    response = client.post("/artist/", json=data, headers=auth_headers)

    # Debugging line to check the response
    print(f'response: {response.get_json()}')
    # Debugging line to check the headers
    print(f'response_headers: {response.headers}')

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
    assert artwork.category_id == data["category_id"]
    assert len(artwork.tags) == 2
    assert {tag.title for tag in artwork.tags} == set(data["tag_names"])
