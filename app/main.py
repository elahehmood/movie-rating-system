from fastapi import FastAPI

app = FastAPI(title="Movie Rating System")

@app.get("/")
def health_check():
    return {"status": "ok"}
