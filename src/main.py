from contextlib import asynccontextmanager

from fastapi import FastAPI

from docs.tags_metadata import tags_metadata
from routes import authentication, ping, users
from setup.database_setup import setup_database
from setup.super_user import create_super_user

@asynccontextmanager
async def lifespan(_app: FastAPI):
    await setup()
    yield
    # Potential stuff to do after shutdown
    pass
app = FastAPI(
    title="DnD Tools API",
    summary="An API handling the business logic and static data of the DnD Tool Website.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/",
    openapi_tags=tags_metadata,
)

app.include_router(authentication.router)
app.include_router(ping.router)
app.include_router(users.router)

async def setup():
    await create_super_user()
    await setup_database()