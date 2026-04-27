from fastapi import FastAPI
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title="creciendo")

# Limpiar y procesar orígenes
raw_origins = settings.CORS_ALLOWED_ORIGINS
allowed_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

print(f"DEBUG: CORS_ALLOWED_ORIGINS configurados: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message":"Hola"}