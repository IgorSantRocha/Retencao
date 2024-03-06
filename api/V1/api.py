from fastapi import APIRouter

from api.V1.endpoints import abertura
from api.V1.endpoints import respostas

api_router = APIRouter()
api_router.include_router(
    abertura.router, prefix='/abertura', tags=["Abertura"])

api_router.include_router(
    respostas.router, prefix='/respostas', tags=["Respostas"])
