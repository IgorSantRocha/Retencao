from pydoc import Doc
from fastapi import APIRouter
from core.deps import get_session
from schemas.respostas_schema import MessageSchema, ResponseEvolution
from core.respostas_core import manda_resposta
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status


router = APIRouter()

api_versao = 'api/V1'


@router.post(path="/chatbot", status_code=status.HTTP_201_CREATED,
             summary='Envia retorno chatbot',
             description='Realiza o envio da resposta via WPP com base no callid da OS',
             response_description='Mensagem enviada',
             response_model=ResponseEvolution)
async def post_chatbot(info_messagem: MessageSchema, db: AsyncSession = Depends(get_session)):
    '''Chama a função que trata as informações enviadas'''
    txt_resposta = await manda_resposta(info_messagem=info_messagem, db=db)
    ''''''
    return txt_resposta
