from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.product_schema import (
    CreateProductSchema,
    UpdateProductSchema,
    ProductResponseSchema,
)
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "/",
    response_model=ProductResponseSchema,
)
def create_product(
    payload: CreateProductSchema,
    db: Session = Depends(get_db),
):
    return ProductService.create_product(
        db,
        payload,
    )


@router.get(
    "/",
    response_model=list[ProductResponseSchema],
)
def get_products(
    db: Session = Depends(get_db),
):
    return ProductService.get_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponseSchema,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = ProductService.get_product(
        db,
        product_id,
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponseSchema,
)
def update_product(
    product_id: int,
    payload: UpdateProductSchema,
    db: Session = Depends(get_db),
):
    product = ProductService.update_product(
        db,
        product_id,
        payload,
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = ProductService.delete_product(
        db,
        product_id,
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return {"message": "Product deleted"}
