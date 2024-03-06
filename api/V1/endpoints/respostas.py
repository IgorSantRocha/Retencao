from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from datetime import datetime
from core.request import RequestClient
# from sqlalchemy import delete

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from models.abertura_model import ProjetoFdModel, ProjetoCtbseqModel, RetencaoHistAbModel
from models.abertura_model import OcorrenciasModel, TiposModel, RetencaoAbModel
from schemas.abertura_shema import ProjetoSchema, OcorrenciaSchema, TiposSchema, RetencaoAbSchema, RetencaoRtSchema
from core.deps import get_session

router = APIRouter()

api_versao = 'api/V1'


@router.post(path="/chatbot")
async def request():
    client = RequestClient(
        method='POST',
        url='http://192.168.0.213:3000/message/sendText/chatbot-receptivo',
        headers={
            'apikey': 'rJ9aWxBaX82Pn7vC15tlL5ZBoCwCTLtnvj73OxsycfcI1o84vv9Y2Hh2I2jFNKx9iQVUqteUOk4pWI7g'},
        request_data={
            "number": "5511972339756@s.whatsapp.net",
            "options": {
                "delay": 1200,
                "presence": "composing",
                "linkPreview": "false"
            },
            "textMessage": {
                "text": "Teste resposta API"
            }
        }
    )
    response = await client.send_api_request()
    return response
