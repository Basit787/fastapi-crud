def test_get_products_public(client, db_session):
    from app.products.model import Product

    db_session.add(
        Product(name="Laptop", description="Portable computer", price=1200.0)
    )
    db_session.commit()

    response = client.get("/products/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_product_public(client, db_session):
    from app.products.model import Product

    product = Product(name="Tablet", description="Touch device", price=500.0)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.get(f"/products/{product.id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Tablet"


def test_get_product_not_found(client):
    response = client.get("/products/999")

    assert response.status_code == 404


def test_create_product_requires_auth(client):
    response = client.post(
        "/products/",
        json={"name": "Phone", "description": "Mobile", "price": 800.0},
    )

    assert response.status_code == 401


def test_create_product_manager_allowed(client, manager_headers):
    response = client.post(
        "/products/",
        headers=manager_headers,
        json={"name": "Phone", "description": "Mobile", "price": 800.0},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Phone"


def test_create_product_user_forbidden(client, user_headers):
    response = client.post(
        "/products/",
        headers=user_headers,
        json={"name": "Denied", "description": "Blocked", "price": 1.0},
    )

    assert response.status_code == 403


def test_update_product_manager_allowed(client, manager_headers, db_session):
    from app.products.model import Product

    product = Product(name="Watch", description="Wearable", price=300.0)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.put(
        f"/products/{product.id}",
        headers=manager_headers,
        json={"name": "Smart Watch", "description": "Updated", "price": 350.0},
    )

    assert response.status_code == 200
    assert response.json()["price"] == 350.0


def test_update_product_not_found(client, admin_headers):
    response = client.put(
        "/products/999",
        headers=admin_headers,
        json={"name": "Missing", "description": "Missing", "price": 1.0},
    )

    assert response.status_code == 404


def test_delete_product_admin_allowed(client, admin_headers, db_session):
    from app.products.model import Product

    product = Product(name="Monitor", description="Display", price=250.0)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.delete(f"/products/{product.id}", headers=admin_headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted"}


def test_delete_product_user_forbidden(client, user_headers, db_session):
    from app.products.model import Product

    product = Product(name="Keyboard", description="Input", price=80.0)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.delete(f"/products/{product.id}", headers=user_headers)

    assert response.status_code == 403


def test_delete_product_not_found(client, admin_headers):
    response = client.delete("/products/999", headers=admin_headers)

    assert response.status_code == 404
