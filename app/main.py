from fastapi import FastAPI
from app.controller.router import api_router
from app.core.logging_config import setup_logging

setup_logging()
app = FastAPI()

# Include API router
app.include_router(api_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
