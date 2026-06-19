from pydantic import BaseModel
from pydantic import EmailStr

from app.models.roles import Role


class CreateUserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role = Role.USER


class UpdateUserSchema(BaseModel):
    name: str
    email: EmailStr


class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role

    model_config = {"from_attributes": True}
