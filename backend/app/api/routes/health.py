from fastapi import APIRouter, Response

router = APIRouter()

@router.get("/health")
async def healthcheck():
    return {"status": "ok"}

@router.head("/health")
async def health_head():
    return Response(status_code=200)