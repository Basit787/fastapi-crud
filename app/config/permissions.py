from app.models.roles import Role

ROLE_PERMISSIONS: dict[Role, set[str]] = {
    Role.ADMIN: {
        "users:create",
        "users:read",
        "users:update",
        "users:delete",
        "products:create",
        "products:update",
        "products:delete",
    },
    Role.MANAGER: {
        "users:read",
        "products:create",
        "products:update",
        "products:delete",
    },
    Role.USER: {
        "users:read",
        "users:update_self",
    },
}


def has_permission(role: Role, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())
