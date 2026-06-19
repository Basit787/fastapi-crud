from app.config.database import SessionLocal
from app.models.roles import Role
from app.models.users import User
from app.models.products import Product
from app.utils.security import hash_password


def seed_users(db):
    if db.query(User).count() > 0:
        print("Users already seeded")
        return

    users = [
        User(
            name="James",
            email="james@example.com",
            hashed_password=hash_password("password123"),
            role=Role.ADMIN,
        ),
        User(
            name="Jane",
            email="jane@example.com",
            hashed_password=hash_password("password123"),
            role=Role.MANAGER,
        ),
        User(
            name="John",
            email="john@example.com",
            hashed_password=hash_password("password123"),
            role=Role.USER,
        ),
    ]

    db.add_all(users)
    db.commit()


def seed_products(db):
    if db.query(Product).count() > 0:
        print("Products already seeded")
        return

    products = [
        Product(
            name="MacBook Pro",
            description="Apple laptop",
            price=1999,
        ),
        Product(
            name="iPhone",
            description="Apple smartphone",
            price=999,
        ),
    ]

    db.add_all(products)
    db.commit()


def run():
    db = SessionLocal()

    try:
        seed_users(db)
        seed_products(db)

        print("✅ Seed completed")

    finally:
        db.close()


if __name__ == "__main__":
    run()
