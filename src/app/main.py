from fastapi import FastAPI

from lib.database import Base
from lib.database import engine
from app.products.model import Product  # noqa: F401
from app.router import router
from app.users.model import User  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI CRUD",
)

app.include_router(router)
