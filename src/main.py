from fastapi import FastAPI
from routes import authentication, ping, users

app = FastAPI(
    docs_url="/docs",
    redoc_url="/"
)

app.include_router(authentication.router)
app.include_router(ping.router)
app.include_router(users.router)