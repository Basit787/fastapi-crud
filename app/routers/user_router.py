from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session


from app.config.database import get_db
from app.schemas.user_schema import (
    CreateUserSchema,
    UpdateUserSchema,
    UserResponseSchema,
)
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponseSchema,
)
def create_user(
    payload: CreateUserSchema,
    db: Session = Depends(get_db),
):
    return UserService.create_user(
        db,
        payload,
    )


@router.get(
    "/",
    response_model=list[UserResponseSchema],
)
def get_users(
    db: Session = Depends(get_db),
):
    return UserService.get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = UserService.get_user(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponseSchema,
)
def update_user(
    user_id: int,
    payload: UpdateUserSchema,
    db: Session = Depends(get_db),
):
    user = UserService.update_user(
        db,
        user_id,
        payload,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = UserService.delete_user(
        db,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {"message": "User deleted"}
