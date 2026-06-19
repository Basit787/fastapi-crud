from fastapi import FastAPI

from app.config.database import Base, engine

from app.routers.user_router import router as user_router
from app.routers.product_router import router as product_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI CRUD",
)


app.include_router(user_router)
app.include_router(product_router)


@app.get("/")
def health():
    return {"status": "ok"}
