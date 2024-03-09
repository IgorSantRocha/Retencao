from fastapi import APIRouter
from core.deps import get_session
from schemas.respostas_schema import MessageSchema
from core.respostas_core import monta_txt_resposta
from core.respostas_core import monta_resposta
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status


router = APIRouter()

api_versao = 'api/V1'


@router.post(path="/chatbot", status_code=status.HTTP_201_CREATED,
             summary='Envia retorno chatbot',
             description='Realiza o envio da resposta via WPP com base no callid da OS',
             response_description='Mensagem enviada')
async def post_chatbot(info_messagem: MessageSchema, db: AsyncSession = Depends(get_session)):
    txt_resposta = await monta_resposta(info_messagem=info_messagem, db=db)
    ''''''
    return txt_resposta
