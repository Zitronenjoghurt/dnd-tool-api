from contextlib import asynccontextmanager

from fastapi import FastAPI

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
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/"
)

app.include_router(authentication.router)
app.include_router(ping.router)
app.include_router(users.router)

async def setup():
    await create_super_user()
    await setup_database()