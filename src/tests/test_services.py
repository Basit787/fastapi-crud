from app.core.roles import Role
from app.schemas.auth import RegisterSchema
from app.schemas.user import CreateUserSchema
from app.schemas.user import UpdateUserSchema
from app.services.auth import AuthService
from app.services.user import UserService
from fastapi import HTTPException
import pytest


def test_register_creates_user(db_session):
    payload = RegisterSchema(
        name="New User",
        email="new@test.com",
        password="password123",
    )

    user = AuthService.register(db_session, payload)

    assert user.id is not None
    assert user.email == "new@test.com"
    assert user.role == Role.USER


def test_register_duplicate_email_raises(db_session, regular_user):
    payload = RegisterSchema(
        name="Duplicate",
        email=regular_user.email,
        password="password123",
    )

    with pytest.raises(HTTPException) as exc:
        AuthService.register(db_session, payload)

    assert exc.value.status_code == 400


def test_authenticate_valid_credentials(db_session, regular_user):
    user = AuthService.authenticate(
        db_session,
        regular_user.email,
        "password123",
    )

    assert user.id == regular_user.id


def test_authenticate_invalid_password_raises(db_session, regular_user):
    with pytest.raises(HTTPException) as exc:
        AuthService.authenticate(
            db_session,
            regular_user.email,
            "wrong-password",
        )

    assert exc.value.status_code == 401


def test_authenticate_unknown_email_raises(db_session):
    with pytest.raises(HTTPException) as exc:
        AuthService.authenticate(
            db_session,
            "missing@test.com",
            "password123",
        )

    assert exc.value.status_code == 401


def test_login_returns_access_token(db_session, regular_user):
    result = AuthService.login(
        db_session,
        regular_user.email,
        "password123",
    )

    assert result["token_type"] == "bearer"
    assert result["access_token"]


def test_user_service_crud(db_session):
    created = UserService.create_user(
        db_session,
        CreateUserSchema(
            name="Service User",
            email="service@test.com",
            password="password123",
            role=Role.MANAGER,
        ),
    )

    users = UserService.get_users(db_session)
    assert len(users) == 1

    fetched = UserService.get_user(db_session, created.id)
    assert fetched.name == "Service User"

    updated = UserService.update_user(
        db_session,
        created.id,
        UpdateUserSchema(name="Updated", email="updated@test.com"),
    )
    assert updated.email == "updated@test.com"

    deleted = UserService.delete_user(db_session, created.id)
    assert deleted.id == created.id
    assert UserService.get_user(db_session, created.id) is None


def test_user_service_update_and_delete_missing_user(db_session):
    assert (
        UserService.update_user(
            db_session,
            999,
            UpdateUserSchema(name="Missing", email="missing@test.com"),
        )
        is None
    )

    assert UserService.delete_user(db_session, 999) is None
