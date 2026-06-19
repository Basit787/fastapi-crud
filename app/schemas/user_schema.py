from pydantic import BaseModel
from pydantic import EmailStr


class CreateUserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UpdateUserSchema(BaseModel):
    name: str
    email: EmailStr


class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}
