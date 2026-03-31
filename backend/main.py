from fastapi import FastAPI
from backend.database import engine, Base
from contextlib import asynccontextmanager
from backend.routers import lists, items

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(lists.router, prefix="/api")
app.include_router(items.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API läuft!"}