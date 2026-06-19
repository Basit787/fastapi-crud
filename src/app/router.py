from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.products.router import router as product_router
from app.users.router import router as user_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(product_router)


@router.get("/")
def health():
    return {"status": "ok"}
