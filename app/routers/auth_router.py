from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.auth_schema import RegisterSchema
from app.schemas.auth_schema import TokenSchema
from app.schemas.user_schema import UserResponseSchema
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserResponseSchema,
)
def register(
    payload: RegisterSchema,
    db: Session = Depends(get_db),
):
    return AuthService.register(db, payload)


@router.post(
    "/login",
    response_model=TokenSchema,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return AuthService.login(
        db,
        form_data.username,
        form_data.password,
    )
