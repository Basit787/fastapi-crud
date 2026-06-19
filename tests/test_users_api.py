def test_get_users_requires_auth(client):
    response = client.get("/users/")

    assert response.status_code == 401


def test_get_users_as_user(client, user_headers, regular_user):
    response = client.get("/users/", headers=user_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == regular_user.email


def test_create_user_admin_only(client, admin_headers, user_headers):
    payload = {
        "name": "Created",
        "email": "created@test.com",
        "password": "password123",
        "role": "manager",
    }

    forbidden = client.post("/users/", json=payload, headers=user_headers)
    assert forbidden.status_code == 403

    allowed = client.post("/users/", json=payload, headers=admin_headers)
    assert allowed.status_code == 200
    assert allowed.json()["role"] == "manager"


def test_get_user_not_found(client, user_headers):
    response = client.get("/users/999", headers=user_headers)

    assert response.status_code == 404


def test_update_user_admin_can_update_anyone(client, admin_headers, regular_user):
    response = client.put(
        f"/users/{regular_user.id}",
        headers=admin_headers,
        json={"name": "Admin Updated", "email": "admin-updated@test.com"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Admin Updated"


def test_update_user_can_update_self(client, user_headers, regular_user):
    response = client.put(
        f"/users/{regular_user.id}",
        headers=user_headers,
        json={"name": "Self Updated", "email": regular_user.email},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Self Updated"


def test_update_user_cannot_update_others(client, user_headers, admin_user):
    response = client.put(
        f"/users/{admin_user.id}",
        headers=user_headers,
        json={"name": "Blocked", "email": admin_user.email},
    )

    assert response.status_code == 403


def test_update_user_not_found(client, admin_headers):
    response = client.put(
        "/users/999",
        headers=admin_headers,
        json={"name": "Missing", "email": "missing@test.com"},
    )

    assert response.status_code == 404


def test_delete_user_admin_only(client, admin_headers, user_headers, regular_user):
    forbidden = client.delete(
        f"/users/{regular_user.id}",
        headers=user_headers,
    )
    assert forbidden.status_code == 403

    allowed = client.delete(
        f"/users/{regular_user.id}",
        headers=admin_headers,
    )
    assert allowed.status_code == 200
    assert allowed.json() == {"message": "User deleted"}


def test_delete_user_not_found(client, admin_headers):
    response = client.delete("/users/999", headers=admin_headers)

    assert response.status_code == 404
