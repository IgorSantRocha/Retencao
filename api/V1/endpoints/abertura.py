from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from datetime import datetime
# from sqlalchemy import delete

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from models.abertura_model import ProjetoFdModel, ProjetoCtbseqModel, RetencaoHistAbModel
from models.abertura_model import OcorrenciasModel, TiposModel, RetencaoAbModel
from schemas.abertura_shema import ProjetoSchema, OcorrenciaSchema, TiposSchema, RetencaoAbSchema, RetencaoRtSchema
from core.deps import get_session
from crud.crud_abertura import gerar_id_unico

router = APIRouter()

api_versao = 'api/V1'

# GET Projetos


@router.get('/projetos', response_model=List[ProjetoSchema], status_code=status.HTTP_200_OK,
            summary='Lista todos os projetos ativos',
            description='Lista todos os projetos presentes na tabela do CTBFED e do CTBSEQ',
            response_description='Lista obtida com sucesso!')
async def get_projetos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ProjetoFdModel).filter(ProjetoFdModel.PROJETO != '...')
        result = await session.execute(query)
        projetos_fd = result.scalars().all()  # type: ignore

        query = select(ProjetoCtbseqModel).filter(
            ProjetoCtbseqModel.PROJETO != '...')
        result = await session.execute(query)
        projetos_seq = result.scalars().all()  # type: ignore

        projetos = projetos_fd + projetos_seq

        if projetos:
            return projetos
        else:
            raise HTTPException(detail='Nenhum projeto encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# GET Ocorrências
@router.get('/ocorrencias/{projeto}', response_model=List[OcorrenciaSchema], status_code=status.HTTP_200_OK,
            summary='Lista as ocorrências',
            description='Lista as ocorrências de acordo com o projeto expecificado',
            response_description='Lista obtida com sucesso!')
async def get_ocorrencias(projeto: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        projeto = projeto.upper()
        if projeto == 'FISERV':
            projeto = "FIRST"

        query = select(OcorrenciasModel).filter(
            OcorrenciasModel.projeto == projeto).filter(OcorrenciasModel.motivo != '...')

        result = await session.execute(query)
        ocorrencias: List[OcorrenciaSchema] = result.scalars().all()

        if ocorrencias:
            return ocorrencias
        else:
            raise HTTPException(detail='Nenhuma ocorrência encontrada',
                                status_code=status.HTTP_404_NOT_FOUND)


# GET Tipos
@router.get('/tipos/{projeto}', response_model=List[TiposSchema], status_code=status.HTTP_200_OK,
            summary='Lista os tipos de pedido',
            description='Lista os tipos de pedido de acordo com os existentes para o projeto expecificado.',
            response_description='Lista obtida com sucesso!')
async def get_tipos(projeto: str, db: AsyncSession = Depends(get_session)):
    async with db as session:

        if projeto.upper() == 'FISERV':
            projeto = "FIRST"

        if projeto not in ('CIELO', 'CTB', 'CTBPO'):
            query = select(TiposModel)
        else:
            query = select(TiposModel).filter(
                TiposModel.Tipo_Atendimento == 'Desinstalação')

        result = await session.execute(query)
        ocorrencias: List[TiposSchema] = result.scalars().all()

        if ocorrencias:
            return ocorrencias
        else:
            raise HTTPException(detail='Nenhuma tipo de pedido encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Abertura
@router.put('/', response_model=RetencaoRtSchema, status_code=status.HTTP_202_ACCEPTED,
            summary='Realiza a abertura da OS',
            description='Realiza a abertura/reabertura da OS verificando se a OS existeou não e então decidindo entre update/insert',
            response_description='Abertura realizada!')
async def put_abertura_chatbot(info_os: RetencaoAbSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(RetencaoAbModel).filter(
            RetencaoAbModel.os == info_os.os)
        result = await session.execute(query)
        os_up = result.scalar_one_or_none()

        data_hora_atual = datetime.now()

        # Formate a data e hora atual como DD/MM/AAAA HH:MM:SS
        data_hora_formatada = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
        if os_up:
            info_os.projeto = info_os.projeto.upper()
            antigo_historico = os_up.problema_apresentado
            os_up.dt_abertura = datetime.now()
            os_up.telefone_tecnico = info_os.telefone_tecnico
            os_up.ocorrencia = info_os.ocorrencia
            os_up.projeto = info_os.projeto
            os_up.tipo_atendimento = info_os.tipo_atendimento
            os_up.dt_fechamento = datetime.now()

            os_up.subprojeto = os_up.subprojeto or '...'
            os_up.fase = 'D+0'
            os_up.etapa = 'D+0'
            os_up.acao_d1 = '...'
            os_up.acao_D29 = '...'

            # Atribui 'CHATBOT' se atendente_abertura ou nome_tecnico for None
            os_up.atendente_abertura = 'CHATBOT'
            os_up.nome_tecnico = 'CHATBOT'
            os_up.chave = os_up.os
            os_up.tipo = ''

            # projeto
            if info_os.projeto != 'CIELO' and os_up.os.startswith('CLC'):
                os_up.projeto = 'CIELO'
            elif info_os.projeto == 'CIELO' and not os_up.os.startswith('CLC'):
                os_up.projeto = 'CTBPO'
            elif info_os.projeto == 'FISERV':
                os_up.projeto = 'FIRST'

            # regra para criar ocorrência que será usada somente no código
            # 16/02/24 - Comentando essa regra para deixar os CIELO(CLC) irem na fila
            '''if os_up.projeto == 'CIELO' and info_os.ocorrencia not in (
                    'Técnico em rota', 'Coleta realizada c/ sucesso', 'Insucesso na visita'):
                _ocorrencia = 'Insucesso na visita'
            else:
                _ocorrencia = info_os.ocorrencia'''
            _ocorrencia = info_os.ocorrencia  # Definindo valor padrão para a variável existir

            # Verifica se o ocorrencia está entre os valores especificados
            os_up.retorno_tecnico = 'Sim' if _ocorrencia in (
                'Técnico em rota', 'Coleta realizada c/ sucesso', 'Insucesso na visita') else 'Não'

            # status
            if _ocorrencia == 'Técnico em rota':
                os_up.status = 'SEGUIR ROTA - MENSAGEM ENVIADA'
            elif _ocorrencia == 'Insucesso na visita' and os_up.os.startswith('CLC'):
                os_up.status = 'INSUCESSO - SEGUIR ROTA'
            elif _ocorrencia == 'Coleta realizada c/ sucesso':
                os_up.status = 'PEDIDO REALIZADO'
            else:
                os_up.status = '...'

            # conclusao
            if _ocorrencia == 'Técnico em rota':
                os_up.conclusao_operador = 'Enviada mensagem no WhatsApp'
            elif _ocorrencia == 'Insucesso na visita' and os_up.os.startswith('CLC'):
                os_up.conclusao_operador = 'Seguir rota'
            elif _ocorrencia == 'Coleta realizada c/ sucesso':
                os_up.conclusao_operador = 'Informação de coleta recebida. Técnico autorizado a seguir rota.'
            else:
                os_up.conclusao_operador = ''

            # Definicao
            if _ocorrencia == 'Técnico em rota':
                os_up.definicao = 'PENDENTE / EM ROTA'
            elif _ocorrencia == 'Insucesso na visita' and info_os.os.startswith('CLC'):
                os_up.definicao = 'MIGROU CAÇA-POS'
            elif _ocorrencia == 'Coleta realizada c/ sucesso':
                os_up.definicao = 'PEDIDO REALIZADO'
            else:
                os_up.definicao = ''

            # satatus relatorio
            if _ocorrencia == 'Técnico em rota':
                os_up.status_relatorio = 'PENDENTE / EM ROTA'
            elif _ocorrencia == 'Insucesso na visita' and info_os.os.startswith('CLC'):
                os_up.status_relatorio = 'SOLICITAÇÃO DE CANCELAMENTO'
            elif _ocorrencia == 'Coleta realizada c/ sucesso':
                os_up.status_relatorio = 'SEM TRATATIVA DA CENTRAL'
            else:
                os_up.status_relatorio = ''

            nova_obs = f'|{data_hora_formatada} - Técnico: {os_up.nome_tecnico} - Ocorrência: {info_os.ocorrencia}  - {info_os.problema_apresentado}'
            os_up.problema_apresentado = antigo_historico + f'\n' + nova_obs

            cliente_query = select(ProjetoFdModel.Cliente).filter(
                ProjetoFdModel.PROJETO == info_os.projeto)

            cliente_result = await session.execute(cliente_query)

            os_up.cliente = cliente_result.scalar_one_or_none()

            if not os_up.cliente:
                cliente_query = select(ProjetoCtbseqModel.Cliente).filter(
                    ProjetoCtbseqModel.PROJETO == info_os.projeto)

                cliente_result = await session.execute(cliente_query)
                os_up.cliente = cliente_result.scalar_one_or_none()

            os_up.call_id = gerar_id_unico()

            # coloco a versão da API
            os_up.versao = api_versao

            # Salvar as alterações no banco de dados, se necessário
            session.add(os_up)
            await session.commit()

        else:
            info_os.projeto = info_os.projeto.upper()
            os_up = RetencaoAbModel(
                os=info_os.os,
                dt_abertura=datetime.now())

            os_up.telefone_tecnico = info_os.telefone_tecnico
            os_up.ocorrencia = info_os.ocorrencia
            os_up.projeto = info_os.projeto
            os_up.tipo_atendimento = info_os.tipo_atendimento
            # regras para encontrar o cliente de acordo com o projeto
            os_up.dt_fechamento = datetime.now()

            os_up.subprojeto = os_up.subprojeto or '...'
            os_up.fase = os_up.fase or 'D+0'
            os_up.etapa = os_up.etapa or 'D+0'
            os_up.acao_d1 = os_up.acao_d1 or '...'
            os_up.acao_D29 = os_up.acao_D29 or '...'

            # Atribui 'CHATBOT' se atendente_abertura ou nome_tecnico for None
            os_up.atendente_abertura = os_up.atendente_abertura or 'CHATBOT'
            os_up.nome_tecnico = os_up.nome_tecnico or 'CHATBOT'
            os_up.chave = os_up.chave or os_up.os
            os_up.tipo = ''

            # projeto
            if info_os.projeto != 'CIELO' and os_up.os.startswith('CLC'):
                os_up.projeto = 'CIELO'
            elif info_os.projeto == 'CIELO' and not os_up.os.startswith('CLC'):
                os_up.projeto = 'CTBPO'
            elif info_os.projeto == 'FISERV':
                os_up.projeto = 'FIRST'

            # regra para criar ocorrência que será usada somente no código
            if os_up.projeto == 'CIELO' and info_os.ocorrencia not in (
                    'Técnico em rota', 'Coleta realizada c/ sucesso', 'Insucesso na visita'):
                _ocorrencia = 'Insucesso na visita'
            else:
                _ocorrencia = info_os.ocorrencia

            # Verifica se o ocorrencia está entre os valores especificados
            os_up.retorno_tecnico = 'Sim' if _ocorrencia in (
                'Técnico em rota', 'Coleta realizada c/ sucesso', 'Insucesso na visita') else 'Não'

            # status
            if _ocorrencia == 'Técnico em rota':
                os_up.status = 'SEGUIR ROTA - MENSAGEM ENVIADA'
            elif _ocorrencia == 'Insucesso na visita' and os_up.os.startswith('CLC'):
                os_up.status = 'INSUCESSO - SEGUIR ROTA'
            elif _ocorrencia == 'Coleta realizada c/ sucesso':
                os_up.status = 'PEDIDO REALIZADO'
            else:
                os_up.status = '...'

            # conclusao
            if _ocorrencia == 'Técnico em rota':
                os_up.conclusao_operador = 'Enviada mensagem no WhatsApp'
            elif _ocorrencia == 'Insucesso na visita' and os_up.os.startswith('CLC'):
                os_up.conclusao_operador = 'Seguir rota'
            elif _ocorrencia == 'Coleta realizada c/ sucesso':
                os_up.conclusao_operador = 'Informação de coleta recebida. Técnico autorizado a seguir rota.'
            else:
                os_up.conclusao_operador = ''

            # Definicao
            if _ocorrencia == 'Técnico em rota':
                os_up.definicao = 'PENDENTE / EM ROTA'
            elif _ocorrencia == 'Insucesso na visita' and os_up.os.startswith('CLC'):
                os_up.definicao = 'MIGROU CAÇA-POS'
            elif _ocorrencia == 'Coleta realizada c/ sucesso':
                os_up.definicao = 'PEDIDO REALIZADO'
            else:
                os_up.definicao = ''

            # satatus relatorio
            if _ocorrencia == 'Técnico em rota':
                os_up.status_relatorio = 'PENDENTE / EM ROTA'
            elif _ocorrencia == 'Insucesso na visita' and os_up.os.startswith('CLC'):
                os_up.status_relatorio = 'SOLICITAÇÃO DE CANCELAMENTO'
            elif _ocorrencia == 'Coleta realizada c/ sucesso':
                os_up.status_relatorio = 'SEM TRATATIVA DA CENTRAL'
            else:
                os_up.status_relatorio = ''

            nova_obs = f'|{data_hora_formatada} - Técnico: {os_up.nome_tecnico} - Ocorrência: {info_os.ocorrencia}  - {info_os.problema_apresentado}'
            os_up.problema_apresentado = nova_obs

            cliente_query = select(ProjetoFdModel.Cliente).filter(
                ProjetoFdModel.PROJETO == info_os.projeto)

            cliente_result = await session.execute(cliente_query)
            os_up.cliente = cliente_result.scalar_one_or_none()

            if not os_up.cliente:
                cliente_query = select(ProjetoCtbseqModel.Cliente).filter(
                    ProjetoCtbseqModel.PROJETO == info_os.projeto)

                cliente_result = await session.execute(cliente_query)
                os_up.cliente = cliente_result.scalar_one_or_none()

            os_up.call_id = gerar_id_unico()

            # coloco a versão da API
            os_up.versao = api_versao

            session.add(os_up)

            # Commit explicitamente a transação
            await session.commit()

        # Regras para inserir também na tabela de hintórico
        os_hist = RetencaoHistAbModel(
            os=os_up.os,
            problema_apresentado=nova_obs,
            tecnico=os_up.nome_tecnico,
            callid=os_up.call_id
        )
        session.add(os_hist)

        # Commit explicitamente a transação
        await session.commit()

        # Retornar o objeto atualizado
        return os_up
