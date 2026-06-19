from collections.abc import Callable

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.auth.dependencies import get_current_user
from app.auth.permissions import has_permission
from lib.roles import Role
from app.users.model import User


def require_permission(permission: str) -> Callable:
    def permission_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if not has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return permission_checker


def require_roles(*roles: Role) -> Callable:
    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker


def require_admin_or_self(
    user_id: int,
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role == Role.ADMIN:
        return current_user

    if current_user.id == user_id and has_permission(
        current_user.role,
        "users:update_self",
    ):
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions",
    )
