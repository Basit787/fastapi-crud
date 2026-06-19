from fastapi import FastAPI

from app.api.router import api_router
from app.core.database import Base
from app.core.database import engine
from app.models.product import Product  # noqa: F401
from app.models.user import User  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI CRUD",
)

app.include_router(api_router)
