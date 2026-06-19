from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.user_schema import CreateUserSchema
from app.schemas.user_schema import UpdateUserSchema
from app.utils.security import hash_password


class UserService:
    @staticmethod
    def create_user(
        db: Session,
        payload: CreateUserSchema,
    ):
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
    def get_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_user(
        db: Session,
        user_id: int,
    ):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        payload: UpdateUserSchema,
    ):
        user = UserService.get_user(
            db,
            user_id,
        )

        if not user:
            return None

        user.name = payload.name
        user.email = payload.email

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_user(
        db: Session,
        user_id: int,
    ):
        user = UserService.get_user(
            db,
            user_id,
        )

        if not user:
            return None

        db.delete(user)
        db.commit()

        return user
