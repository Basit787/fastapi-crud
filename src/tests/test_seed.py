from app.auth.security import hash_password
from app.products.model import Product
from app.users.model import User
from lib.roles import Role
from lib.seed import seed_products
from lib.seed import seed_users


def test_seed_users_skips_when_data_exists(db_session):
    db_session.add(
        User(
            name="Existing",
            email="existing@test.com",
            hashed_password=hash_password("password123"),
            role=Role.USER,
        )
    )
    db_session.commit()
    seed_users(db_session)
    assert db_session.query(User).count() == 1


def test_seed_users_creates_defaults(db_session):
    seed_users(db_session)
    users = db_session.query(User).all()
    assert len(users) == 3
    assert {user.role for user in users} == {Role.ADMIN, Role.MANAGER, Role.USER}


def test_seed_products_skips_when_data_exists(db_session):
    db_session.add(
        Product(name="Existing", description="Exists", price=1.0),
    )
    db_session.commit()
    seed_products(db_session)
    assert db_session.query(Product).count() == 1


def test_seed_products_creates_defaults(db_session):
    seed_products(db_session)
    products = db_session.query(Product).all()
    assert len(products) == 2
