import httpx
from core.request import RequestClient, RequestEvolutionAPI
from crud.crud_respostas import limpa_callid
from schemas.respostas_schema import MessageSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
import crud
from pydoc import Doc


def monta_txt_resposta(os: str, atendente: str, conclusao: str, obs: str, protocolo_aut: bool, protocolo: str):
    '''Esta função faz apenas um concatenar das variáveis, montando o texto que será enviado no WPP'''
    enter = "\n"
    txt_retorno = f"*Retorno da OS:* {os}{enter}{enter}*Atendente:*{atendente}{enter}*Observações:*{enter}{conclusao}{enter}{obs}"
    if protocolo_aut:
        txt_retorno = f'{txt_retorno}{enter}{enter}*Anote o protocolo:* {protocolo}'
    return txt_retorno


async def manda_resposta(info_messagem: MessageSchema, db: AsyncSession):
    '''Chama as funções necessárias para obter as informações e envia a requisição para o EvolutionAPI'''
    info_callid = await crud.valida_callid(db=db, callid=info_messagem.callid)
    if not info_callid:
        '''Vou criar essa regra depois'''
        info_callid = 'Nenhum callid pendente encontrado!'
        return info_callid

    # Busco a conclusão e a informação para saber se foi protocolada ou não
    info_conclusao = await crud.busca_conclusao(db=db, codigo=info_messagem.codigo_conclusao)
    protocolo_aut = info_conclusao.protocolo

    # Monto o corpo da requisição
    client = RequestEvolutionAPI(
        instance='chatbot-receptivo',
        telefone=info_messagem.telefone,
        msg=monta_txt_resposta(
            info_messagem.os,
            info_messagem.atendente,
            info_conclusao.conclusao_operador,
            info_messagem.obs,
            protocolo_aut,
            info_messagem.protocolo)
    )

    # manda a request ou erro 400
    try:
        response = await client.send_api_request()
    except httpx.HTTPStatusError as exc:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    # se enviou com sucesso a requisição, limpo o callid da TB_Projeto_Fedex
    await limpa_callid(callid=info_messagem.callid, db=db)

    return response
