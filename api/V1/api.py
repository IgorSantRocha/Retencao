from fastapi import APIRouter

from api.V1.endpoints import abertura

api_router = APIRouter()
api_router.include_router(
    abertura.router, prefix='/abertura', tags=["Abertura"])
