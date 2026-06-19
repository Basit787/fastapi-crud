import jwt
from collections.abc import Callable

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import has_permission
from app.core.roles import Role
from app.core.security import decode_access_token
from app.models.user import User
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError as exc:
        raise credentials_exception from exc

    user = UserService.get_user(db, int(user_id))

    if not user:
        raise credentials_exception

    return user


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
