from app.schemas.product_schema import CreateProductSchema
from app.schemas.product_schema import UpdateProductSchema
from app.services.product_service import ProductService


def test_product_service_crud(db_session):
    created = ProductService.create_product(
        db_session,
        CreateProductSchema(
            name="Phone",
            description="Smartphone",
            price=999.0,
        ),
    )

    products = ProductService.get_products(db_session)
    assert len(products) == 1

    fetched = ProductService.get_product(db_session, created.id)
    assert fetched.name == "Phone"

    updated = ProductService.update_product(
        db_session,
        created.id,
        UpdateProductSchema(
            name="Updated Phone",
            description="Updated",
            price=899.0,
        ),
    )
    assert updated.price == 899.0

    deleted = ProductService.delete_product(db_session, created.id)
    assert deleted.id == created.id
    assert ProductService.get_product(db_session, created.id) is None


def test_product_service_update_and_delete_missing_product(db_session):
    assert (
        ProductService.update_product(
            db_session,
            999,
            UpdateProductSchema(name="Missing", description="Missing", price=1.0),
        )
        is None
    )

    assert ProductService.delete_product(db_session, 999) is None
