from fastapi import APIRouter

from app.api.endpoints import auth
from app.api.endpoints import products
from app.api.endpoints import users

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(products.router)


@api_router.get("/")
def health():
    return {"status": "ok"}
