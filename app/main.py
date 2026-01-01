from fastapi import FastAPI
from app.controller.router import api_router

app = FastAPI()

# Include API router
app.include_router(api_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
