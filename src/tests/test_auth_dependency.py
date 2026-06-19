from tests.conftest import bearer_headers


def test_invalid_token_returns_401(client):
    response = client.get(
        "/users/",
        headers=bearer_headers("not-a-valid-token"),
    )

    assert response.status_code == 401


def test_token_for_missing_user_returns_401(client, invalid_user_token_headers):
    response = client.get("/users/", headers=invalid_user_token_headers)

    assert response.status_code == 401


def test_token_without_subject_returns_401(client):
    import jwt

    from app.core.config import JWT_ALGORITHM
    from app.core.config import JWT_SECRET_KEY

    token = jwt.encode({"exp": 9999999999}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    response = client.get("/users/", headers=bearer_headers(token))

    assert response.status_code == 401
