def test_get_all_artworks_no_artworks(client):
    response = client.get("/store/artworks")
    assert response.status_code == 404
    data = response.get_json()
    assert data["status"] == "error"
    assert data["message"] == "No artworks found"


def test_get_all_artworks_with_artwork(client, create_artwork):
    # create one artwork via artist endpoint
    artwork_id = create_artwork()
    response = client.get("/store/artworks")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list) and len(data["data"]) == 1
    item = data["data"][0]
    assert item["id"] == artwork_id
    assert item["title"] is not None


def test_get_single_artwork_not_found(client):
    response = client.get("/store/artworks/999")
    assert response.status_code == 404
    data = response.get_json()
    print(data)
    assert "Artwork with id 999 not found" in data["message"]


def test_get_single_artwork_success(client, create_artwork):
    artwork_id = create_artwork()
    response = client.get(f"/store/artworks/{artwork_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    payload = data["data"]
    assert payload["id"] == artwork_id
    assert payload["title"] is not None


def test_upvote_artwork_unauthorized(client):
    # no auth header
    response = client.post("/store/artworks/1/upvote")
    assert response.status_code == 401


def test_upvote_and_duplicate(client, auth_headers, create_artwork):
    artwork_id = create_artwork()
    # first upvote
    r1 = client.post(
        f"/store/artworks/{artwork_id}/upvote",
        headers=auth_headers)
    assert r1.status_code == 200
    d1 = r1.get_json()
    assert d1["status"] == "success"
    # duplicate upvote
    r2 = client.post(
        f"/store/artworks/{artwork_id}/upvote",
        headers=auth_headers)
    assert r2.status_code == 500
    d2 = r2.get_json()
    assert d2["status"] == "error"
    assert "already upvoted" in d2["message"].lower()


def test_remove_upvote_and_not_found(client, auth_headers, create_artwork):
    artwork_id = create_artwork()
    # upvote once
    client.post(f"/store/artworks/{artwork_id}/upvote", headers=auth_headers)
    # remove upvote
    r1 = client.delete(
        f"/store/artworks/{artwork_id}/upvote", headers=auth_headers)
    assert r1.status_code == 200
    d1 = r1.get_json()
    assert d1["status"] == "success"
    # remove again → error
    r2 = client.delete(
        f"/store/artworks/{artwork_id}/upvote", headers=auth_headers)
    assert r2.status_code == 400
    d2 = r2.get_json()
    assert d2["status"] == "error"
    assert "no upvote" in d2["message"].lower()


def test_upvotes_count(client, auth_headers, create_artwork):
    artwork_id = create_artwork()
    # count == 0 initially
    r0 = client.get(f"/store/artworks/{artwork_id}/upvotes")
    assert r0.status_code == 200
    assert r0.get_json()["data"]["upvotes"] == 0
    # upvote twice from same user only counts once
    client.post(f"/store/artworks/{artwork_id}/upvote", headers=auth_headers)
    client.post(f"/store/artworks/{artwork_id}/upvote", headers=auth_headers)
    r1 = client.get(f"/store/artworks/{artwork_id}/upvotes")
    assert r1.status_code == 200
    assert r1.get_json()["data"]["upvotes"] == 1
