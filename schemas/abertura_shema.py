from typing import Optional
from datetime import datetime

from pydantic import BaseModel as SCBaseModel


class ProjetoSchema(SCBaseModel):
    PROJETO: str

    class Config:
        from_attributes = True


class OcorrenciaSchema(SCBaseModel):
    motivo: str

    class Config:
        from_attributes = True


class TiposSchema(SCBaseModel):
    Tipo_Atendimento: str

    class Config:
        from_attributes = True


class RetencaoAbSchema(SCBaseModel):
    # nome_tecnico: Optional[str]
    telefone_tecnico: Optional[str]
    os: str
    problema_apresentado: Optional[str]
    ocorrencia: Optional[str]
    projeto: Optional[str]
    tipo_atendimento: Optional[str]

    class Config:
        from_attributes = True


class RetencaoRtSchema(SCBaseModel):
    dt_abertura: Optional[datetime]
    atendente_abertura: Optional[str]
    retorno_tecnico: Optional[str]
    nome_tecnico: Optional[str]
    telefone_tecnico: Optional[str]
    os: str
    problema_apresentado: Optional[str]
    ocorrencia: Optional[str]
    acao_D29: Optional[str]
    projeto: Optional[str]
    tipo_atendimento: Optional[str]
    status: Optional[str]
    subprojeto: Optional[str]
    cliente: Optional[str]
    versao: Optional[str]
    chave: Optional[str]
    dt_fechamento: Optional[datetime]
    fase: Optional[str]
    conclusao_operador: Optional[str]
    definicao: Optional[str]
    status_relatorio: Optional[str]
    etapa: Optional[str]
    tipo: Optional[str]
    acao_d1: Optional[str]

    class Config:
        from_attributes = True
