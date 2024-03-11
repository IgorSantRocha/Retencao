from pydoc import Doc
from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.respostas_model import RetencaoHistRespModel, RespTbOperacionalModel
from models.respostas_model import RespTbProjetoModel


async def valida_callid(callid: Any, db: AsyncSession) -> Optional[RetencaoHistRespModel]:
    '''
    - Consulta se o callid ainda não teve resposta enviada
    - Caso já tenha sido enviado, retorna a lista vazia
    - Se não, retorna o objeto do tipo RetencaoHistRespModel para ser usado nos updates
    '''
    async with db as session:
        query = select(RetencaoHistRespModel).filter(
            RetencaoHistRespModel.callid == callid, RetencaoHistRespModel.ip.is_(None))
        result = await session.execute(query)
        callid_pendente = result.scalars().all()  # type: ignore

    return callid_pendente


async def busca_conclusao(codigo: str, db: AsyncSession) -> Optional[RespTbOperacionalModel]:
    '''Usa o código de conclusão enviado para obter a conclusão e a informação de Protocolo 0 ou 1'''
    async with db as session:
        query = select(RespTbOperacionalModel).filter(
            RespTbOperacionalModel.codigo == codigo).limit(1)
        result = await session.execute(query)
        info_conclusao = result.scalars().one_or_none()  # type: ignore

    return info_conclusao


async def limpa_callid(callid: Any, db: AsyncSession) -> Optional[RespTbProjetoModel]:
    '''
    - Dá update na TB_PROJETO_FEDEX removendo o call_id
    - Marca na TB_PROJETO_FEDEX_HISTÓRICO como enviada resposta
    '''
    async with db as session:
        # Limpo a TB_Projeto_Fedex
        query = select(RespTbProjetoModel).filter(
            RespTbProjetoModel.call_id == callid).limit(1)
        result = await session.execute(query)
        os_up = result.scalar_one_or_none()
        if os_up:
            os_up.call_id = None
            session.add(os_up)
            await session.commit()

        # marco como enviado na tabela de histórico
        query = select(RetencaoHistRespModel).filter(
            RetencaoHistRespModel.callid == callid).limit(1)
        result = await session.execute(query)
        os_up = result.scalar_one_or_none()
        if os_up:
            os_up.ip = 'Resposta enviada'
            session.add(os_up)
            await session.commit()

    return os_up
