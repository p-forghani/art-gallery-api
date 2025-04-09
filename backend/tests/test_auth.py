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
