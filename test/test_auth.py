def test_register_user(client):
    response = client.post(
        "/register",
        json={
        "username": "Bogdan",
        "password": "1234567"})

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "Bogdan"
    assert "hashed_password" not in data


def test_register_duplicate_user(client):
    client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234567"}
    )
    response = client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234567"}
    )
    assert response.status_code == 400

def test_login_token(client):
    client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234567"}
    )
    response = client.post(
        "/token",
        data={"username": "Bogdan", "password": "1234567"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data

def test_failed_login(client):
    client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234567"}
    )
    response = client.post(
        "/token",
        data={"username": "Bogdan", "password": "123456"}
    )
    assert response.status_code == 401


def test_auth_route(client):
    client.post(
        "/register",
        json={"username": "Bogdan", "password": "1234567"}
    )

    response_for_token = client.post(
        "/token",
        data={"username": "Bogdan", "password": "1234567"}
    )
    data = response_for_token.json()
    token = data["access_token"]

    response = client.get(
        "/ticket",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
