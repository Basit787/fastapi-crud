from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.auth_schema import RegisterSchema
from app.utils.security import create_access_token
from app.utils.security import hash_password
from app.utils.security import verify_password


class AuthService:
    @staticmethod
    def register(
        db: Session,
        payload: RegisterSchema,
    ):
        existing_user = db.query(User).filter(User.email == payload.email).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            name=payload.name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
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
        user = db.query(User).filter(User.email == email).first()

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
