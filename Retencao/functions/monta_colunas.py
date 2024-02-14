from schemas.abertura_shema import RetencaoRtSchema
from models.abertura_model import RetencaoAbModel
from datetime import datetime


def cria_colunas(schema: RetencaoAbModel):
    # Atribui a data atual se dt_abertura for None
    schema.dt_abertura = schema.dt_abertura or datetime.now()
    schema.dt_fechamento = schema.dt_fechamento or datetime.now()

    schema.fase = schema.fase or 'D+0'
    schema.etapa = schema.etapa or 'D+0'
    schema.acao_d1 = schema.acao_d1 or '...'
    schema.acao_D29 = schema.acao_D29 or '...'

    # Atribui 'CHATBOT' se atendente_abertura ou nome_tecnico for None
    schema.atendente_abertura = schema.atendente_abertura or 'CHATBOT'
    schema.nome_tecnico = schema.nome_tecnico or 'CHATBOT'
    schema.chave = schema.chave or schema.os
    schema.tipo = ''

    # Verifica se o ocorrencia está entre os valores especificados
    schema.retorno_tecnico = 'Sim' if schema.ocorrencia in (
        'Técnico em rota', 'Coleta realizada c/ sucesso', 'Insucesso na visita') else 'Não'

    # status
    if schema.ocorrencia == 'Técnico em rota':
        schema.status = 'SEGUIR ROTA - MENSAGEM ENVIADA'
    elif schema.ocorrencia == 'Insucesso na visita' and schema.os.startswith('CLC'):
        schema.status = 'INSUCESSO - SEGUIR ROTA'
    elif schema.ocorrencia == 'Coleta realizada c/ sucesso':
        schema.status = 'PEDIDO REALIZADO'
    else:
        schema.status = '...'

    # conclusao
    if schema.ocorrencia == 'Técnico em rota':
        schema.conclusao_operador = 'Enviada mensagem no WhatsApp'
    elif schema.ocorrencia == 'Insucesso na visita' and schema.os.startswith('CLC'):
        schema.conclusao_operador = 'Seguir rota'
    elif schema.ocorrencia == 'Coleta realizada c/ sucesso':
        schema.conclusao_operador = 'Informação de coleta recebida. Técnico autorizado a seguir rota.'
    else:
        schema.conclusao_operador = ''

    # Definicao
    if schema.ocorrencia == 'Técnico em rota':
        schema.definicao = 'PENDENTE / EM ROTA'
    elif schema.ocorrencia == 'Insucesso na visita' and schema.os.startswith('CLC'):
        schema.definicao = 'MIGROU CAÇA-POS'
    elif schema.ocorrencia == 'Coleta realizada c/ sucesso':
        schema.definicao = 'PEDIDO REALIZADO'
    else:
        schema.definicao = ''

    # satatus relatorio
    if schema.ocorrencia == 'Técnico em rota':
        schema.status_relatorio = 'PENDENTE / EM ROTA'
    elif schema.ocorrencia == 'Insucesso na visita' and schema.os.startswith('CLC'):
        schema.status_relatorio = 'SOLICITAÇÃO DE CANCELAMENTO'
    elif schema.ocorrencia == 'Coleta realizada c/ sucesso':
        schema.status_relatorio = 'SEM TRATATIVA DA CENTRAL'
    else:
        schema.status_relatorio = ''

    # projeto
    if schema.projeto != 'CIELO' and schema.os.startswith('CLC'):
        schema.projeto = 'CIELO'
    elif schema.projeto == 'CIELO' and not schema.os.startswith('CLC'):
        schema.projeto = 'CTBPO'
    elif schema.projeto == 'FISERV':
        schema.projeto = 'FIRST'

    return schema
