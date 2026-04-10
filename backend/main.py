from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.database import engine, Base
from contextlib import asynccontextmanager
from backend.routers import lists, items, tags

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(lists.router, prefix="/api")
app.include_router(items.router, prefix="/api")
app.include_router(tags.router, prefix="/api")

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")