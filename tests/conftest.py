import os

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.config.database import Base
from app.config.database import get_db
from app.main import app
from app.models.roles import Role
from app.models.users import User
from app.utils.security import create_access_token
from app.utils.security import hash_password


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session):
    user = User(
        name="Admin",
        email="admin@test.com",
        hashed_password=hash_password("password123"),
        role=Role.ADMIN,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def manager_user(db_session):
    user = User(
        name="Manager",
        email="manager@test.com",
        hashed_password=hash_password("password123"),
        role=Role.MANAGER,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def regular_user(db_session):
    user = User(
        name="User",
        email="user@test.com",
        hashed_password=hash_password("password123"),
        role=Role.USER,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def login(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def auth_headers(client: TestClient, user: User, password: str = "password123"):
    return login(client, user.email, password)


def bearer_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, admin_user):
    return auth_headers(client, admin_user)


@pytest.fixture
def manager_headers(client, manager_user):
    return auth_headers(client, manager_user)


@pytest.fixture
def user_headers(client, regular_user):
    return auth_headers(client, regular_user)


@pytest.fixture
def invalid_user_token_headers():
    token = create_access_token(9999)
    return bearer_headers(token)
