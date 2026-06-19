from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.schemas import RegisterSchema
from app.auth.schemas import TokenSchema
from app.auth.service import AuthService
from lib.database import get_db
from app.users.schemas import UserResponseSchema

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
