from fastapi import FastAPI
from database import MongoDB
from routes import ping

app = FastAPI(
    docs_url="/docs",
    redoc_url="/"
)

app.include_router(ping.router)