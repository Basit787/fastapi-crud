def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Registered",
            "email": "registered@test.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "registered@test.com"
    assert body["role"] == "user"


def test_register_duplicate_email(client, regular_user):
    response = client.post(
        "/auth/register",
        json={
            "name": "Duplicate",
            "email": regular_user.email,
            "password": "password123",
        },
    )

    assert response.status_code == 400


def test_login(client, regular_user):
    response = client.post(
        "/auth/login",
        data={"username": regular_user.email, "password": "password123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials(client, regular_user):
    response = client.post(
        "/auth/login",
        data={"username": regular_user.email, "password": "wrong-password"},
    )

    assert response.status_code == 401
