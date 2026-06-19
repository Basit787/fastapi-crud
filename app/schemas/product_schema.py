from pydantic import BaseModel


class CreateProductSchema(BaseModel):
    name: str
    description: str
    price: float


class UpdateProductSchema(BaseModel):
    name: str
    description: str
    price: float


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float

    model_config = {"from_attributes": True}
