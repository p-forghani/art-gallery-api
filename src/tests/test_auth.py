def test_register_user(client):
    response = client.post("/auth/register", json={
        "name": "pouria",
        "email": "pouria@example.com",
        "password": "123456"
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Registered"


def test_register_user_already_exists(client):
    # First register the user to ensure they exist
    client.post("/auth/register", json={
        "name": "pouria",
        "email": "pouria@example.com",
        "password": "123456"
    })

    # Attempt to register the same user again
    response = client.post("/auth/register", json={
        "name": "pouria",
        "email": "pouria@example.com",
        "password": "123456"
    })

    assert response.status_code == 409
    data = response.get_json()
    assert data["message"] == "User already exists"


def test_login_user(client):
    # First register
    client.post("/auth/register", json={
        "name": "pouria",
        "email": "pouria@example.com",
        "password": "123456"
    })

    # Then login
    response = client.post("/auth/login", json={
        "email": "pouria@example.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data


def test_logout_user(client):
    # Register and login to get a token
    client.post("/auth/register", json={
        "name": "pouria",
        "email": "pouria@example.com",
        "password": "123456"
    })
    login_resp = client.post("/auth/login", json={
        "email": "pouria@example.com",
        "password": "123456"
    })
    access_token = login_resp.get_json()["access_token"]

    # Logout with the token
    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Successfully logged out"

    # Try to access a protected endpoint with the same token (should be
    # revoked)
    profile_resp = client.get(
        "/auth/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert profile_resp.status_code == 401 or profile_resp.status_code == 422

