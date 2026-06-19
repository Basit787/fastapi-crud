from app.api.deps import require_admin_or_self
from app.api.deps import require_permission
from app.api.deps import require_roles
from app.core.roles import Role
from app.core.security import hash_password
from app.models.user import User
from fastapi import HTTPException
import pytest


def _make_user(user_id: int, role: Role) -> User:
    return User(
        id=user_id,
        name="Test",
        email=f"user{user_id}@test.com",
        hashed_password=hash_password("password123"),
        role=role,
    )


def test_require_permission_allows_authorized_role():
    checker = require_permission("users:read")
    user = _make_user(1, Role.USER)

    assert checker(current_user=user) == user


def test_require_permission_denies_unauthorized_role():
    checker = require_permission("users:create")
    user = _make_user(1, Role.USER)

    with pytest.raises(HTTPException) as exc:
        checker(current_user=user)

    assert exc.value.status_code == 403


def test_require_roles_allows_matching_role():
    checker = require_roles(Role.ADMIN, Role.MANAGER)
    user = _make_user(1, Role.MANAGER)

    assert checker(current_user=user) == user


def test_require_roles_denies_non_matching_role():
    checker = require_roles(Role.ADMIN)
    user = _make_user(1, Role.USER)

    with pytest.raises(HTTPException) as exc:
        checker(current_user=user)

    assert exc.value.status_code == 403


def test_require_admin_or_self_allows_admin():
    admin = _make_user(1, Role.ADMIN)

    assert require_admin_or_self(user_id=99, current_user=admin) == admin


def test_require_admin_or_self_allows_self_update():
    user = _make_user(5, Role.USER)

    assert require_admin_or_self(user_id=5, current_user=user) == user


def test_require_admin_or_self_denies_other_user():
    user = _make_user(5, Role.USER)

    with pytest.raises(HTTPException) as exc:
        require_admin_or_self(user_id=99, current_user=user)

    assert exc.value.status_code == 403
