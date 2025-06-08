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
    response = client.post("/store/upvote/artwork/1")
    assert response.status_code == 401


def test_upvote_artwork_and_duplicate(
        client, auth_headers, create_artwork):
    artwork_id = create_artwork()
    # first upvote
    r1 = client.post(
        f"/store/upvote/artwork/{artwork_id}",
        headers=auth_headers)
    assert r1.status_code == 200
    d1 = r1.get_json()
    assert d1["status"] == "success"

    # duplicate upvote
    r2 = client.post(
        f"/store/upvote/artwork/{artwork_id}",
        headers=auth_headers)
    assert r2.status_code == 500
    d2 = r2.get_json()
    assert d2["status"] == "error"
    assert "already upvoted" in d2["message"].lower()


def test_remove_upvote_and_not_found(client, auth_headers, create_artwork):
    artwork_id = create_artwork()
    # upvote once
    client.post(f"/store/upvote/artwork/{artwork_id}", headers=auth_headers)
    # remove upvote
    r1 = client.delete(
        f"/store/upvote/artwork/{artwork_id}", headers=auth_headers)
    assert r1.status_code == 200
    d1 = r1.get_json()
    assert d1["status"] == "success"
    # remove again → error
    r2 = client.delete(
        f"/store/upvote/artwork/{artwork_id}", headers=auth_headers)
    assert r2.status_code == 400
    d2 = r2.get_json()
    assert d2["status"] == "error"
    assert "no upvote" in d2["message"].lower()


def test_upvotes_count(client, auth_headers, create_artwork):
    artwork_id = create_artwork()
    # count == 0 initially
    r0 = client.get(f"/store/upvote/artwork/{artwork_id}")
    assert r0.status_code == 200
    assert r0.get_json()["data"]["upvotes"] == 0
    # upvote twice from same user only counts once
    client.post(f"/store/upvote/artwork/{artwork_id}", headers=auth_headers)
    client.post(f"/store/upvote/artwork/{artwork_id}", headers=auth_headers)
    r1 = client.get(f"/store/upvote/artwork/{artwork_id}")
    assert r1.status_code == 200
    assert r1.get_json()["data"]["upvotes"] == 1


def test_add_comment(client, auth_headers, create_artwork):
    artwork_id = create_artwork()
    data = {
        "content": "Wow, very beautiful!"
    }

    # Test adding a comment to an artwork
    r1 = client.post(
        f"/store/artworks/{artwork_id}/comments",
        json=data,
        headers=auth_headers
    )
    assert r1.status_code == 201
    assert r1.get_json()['message'] == 'Comment added successfully'

    # Test getting all comments of an artwork
    r2 = client.get(
        f"/store/artworks/{artwork_id}/comments",
    )
    assert r2.status_code == 200
    data = r2.get_json()['data']
    assert data[0]['content'] == "Wow, very beautiful!"


def test_reply_comment(
        client, auth_headers, create_artwork, general_auth_headers
):
    artwork_id = create_artwork()
    data = {
        "content": "Wow, very beautiful!"
    }

    client.post(
        f"/store/artworks/{artwork_id}/comments",
        json=data,
        headers=general_auth_headers
    )

    # Reply with invalid data
    r = client.post(
        "/store/comments/1",
        json={},
        headers=auth_headers
    )
    assert r.status_code == 400

    # Reply with invalid data
    r = client.post(
        "/store/comments/4",
        json={'content': 'good'},
        headers=auth_headers
    )
    assert r.status_code == 404

    reply = {
        'content': 'Thank you!'
    }
    # Reply with valid data
    r2 = client.post(
        "/store/comments/1",
        json=reply,
        headers=auth_headers
    )
    assert r2.status_code == 201


def test_delete_comment(
        client, create_artwork, general_auth_headers, auth_headers
):
    artwork_id = create_artwork()
    # Add comment to artwork by general user
    r = client.post(
        f"/store/artworks/{artwork_id}/comments",
        json={'content': 'Hello World!'},
        headers=general_auth_headers
    )
    comment_id = r.get_json()['comment_id']

    # Delete comment unauthorised
    r2 = client.delete(
        f"/store/comments/{comment_id}"
    )
    assert r2.status_code == 401
    assert r2.get_json()['msg'] == 'Missing Authorization Header'

    # Delete a comment that doesn't belong to the user
    r2 = client.delete(
        f"/store/comments/{comment_id}",
        headers=auth_headers
    )
    assert r2.status_code == 403

    # Delete a comment authenticated and authorised
    r3 = client.delete(
        f"/store/comments/{comment_id}",
        headers=general_auth_headers
    )
    assert r3.status_code == 200
    assert r3.get_json()['status'] == 'success'


def test_upvote_comment_unauthorized(client):
    # no auth header
    response = client.post("/store/upvote/comment/1")
    assert response.status_code == 401


def test_upvote_comment_and_duplicate(
        client, auth_headers, comment_artwork):
    comment_id = comment_artwork()
    # first upvote
    r1 = client.post(
        f"/store/upvote/comment/{comment_id}",
        headers=auth_headers)
    assert r1.status_code == 200
    d1 = r1.get_json()
    assert d1["status"] == "success"

    # duplicate upvote
    r2 = client.post(
        f"/store/upvote/comment/{comment_id}",
        headers=auth_headers)
    assert r2.status_code == 500
    d2 = r2.get_json()
    assert d2["status"] == "error"
    assert "already upvoted" in d2["message"].lower()


def test_remove_comment_upvote_and_not_found(
        client, auth_headers, comment_artwork):
    comment_id = comment_artwork()
    # upvote once
    client.post(f"/store/upvote/comment/{comment_id}", headers=auth_headers)
    # remove upvote
    r1 = client.delete(
        f"/store/upvote/comment/{comment_id}", headers=auth_headers)
    assert r1.status_code == 200
    d1 = r1.get_json()
    assert d1["status"] == "success"
    # remove again → error
    r2 = client.delete(
        f"/store/upvote/comment/{comment_id}", headers=auth_headers)
    assert r2.status_code == 400
    d2 = r2.get_json()
    assert d2["status"] == "error"
    assert "no upvote" in d2["message"].lower()


def test_comment_upvotes_count(client, auth_headers, comment_artwork):
    comment_id = comment_artwork()
    # count == 0 initially
    r0 = client.get(f"/store/upvote/comment/{comment_id}")
    assert r0.status_code == 200
    assert r0.get_json()["data"]["upvotes"] == 0
    # upvote twice from same user only counts once
    client.post(f"/store/upvote/comment/{comment_id}", headers=auth_headers)
    client.post(f"/store/upvote/comment/{comment_id}", headers=auth_headers)
    r1 = client.get(f"/store/upvote/comment/{comment_id}")
    assert r1.status_code == 200
    assert r1.get_json()["data"]["upvotes"] == 1
