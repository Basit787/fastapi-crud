from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.auth.schemas import RegisterSchema
from app.auth.security import create_access_token
from app.auth.security import hash_password
from app.auth.security import verify_password
from lib.roles import Role
from app.users.model import User
from app.users.service import UserService


class AuthService:
    @staticmethod
    def register(
        db: Session,
        payload: RegisterSchema,
    ):
        if UserService.get_user_by_email(db, payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            name=payload.name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
            role=Role.USER,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def authenticate(
        db: Session,
        email: str,
        password: str,
    ):
        user = UserService.get_user_by_email(db, email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ):
        user = AuthService.authenticate(db, email, password)
        access_token = create_access_token(user.id)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
