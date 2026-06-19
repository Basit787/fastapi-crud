from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import CreateProductSchema
from app.schemas.product import UpdateProductSchema


class ProductService:
    @staticmethod
    def create_product(
        db: Session,
        payload: CreateProductSchema,
    ):
        product = Product(
            name=payload.name,
            description=payload.description,
            price=payload.price,
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def get_products(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_product(
        db: Session,
        product_id: int,
    ):
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        payload: UpdateProductSchema,
    ):
        product = ProductService.get_product(db, product_id)

        if not product:
            return None

        product.name = payload.name
        product.description = payload.description
        product.price = payload.price

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
    ):
        product = ProductService.get_product(db, product_id)

        if not product:
            return None

        db.delete(product)
        db.commit()

        return product
