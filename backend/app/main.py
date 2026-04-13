from fastapi import FastAPI
from app.api.router import api_router

from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title="creciendo")

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message":"Hola"}