from app.auth.permissions import has_permission
from lib.roles import Role


def test_admin_has_all_permissions():
    assert has_permission(Role.ADMIN, "users:create")
    assert has_permission(Role.ADMIN, "users:delete")
    assert has_permission(Role.ADMIN, "products:create")


def test_manager_permissions():
    assert has_permission(Role.MANAGER, "users:read")
    assert has_permission(Role.MANAGER, "products:create")
    assert not has_permission(Role.MANAGER, "users:create")
    assert not has_permission(Role.MANAGER, "users:delete")


def test_user_permissions():
    assert has_permission(Role.USER, "users:read")
    assert has_permission(Role.USER, "users:update_self")
    assert not has_permission(Role.USER, "products:create")
    assert not has_permission(Role.USER, "users:delete")


def test_unknown_permission_returns_false():
    assert not has_permission(Role.USER, "unknown:permission")
