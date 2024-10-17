from fastapi import FastAPI

from routes import ping

app = FastAPI(
    docs_url="/docs",
    redoc_url="/"
)

app.include_router(ping.router)