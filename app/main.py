from fastapi import FastAPI
from app.config.database import Base, engine
from app.routers.router import router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI CRUD",
)

app.include_router(router)


@app.get("/")
def health():
    return {"status": "ok"}
