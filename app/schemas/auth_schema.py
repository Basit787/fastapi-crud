from pydantic import BaseModel
from pydantic import EmailStr


class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
