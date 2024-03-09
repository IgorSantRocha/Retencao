from sqlalchemy import Column, Integer, String, Boolean
from core.configs import settings
from datetime import datetime


class RetencaoHistRespModel(settings.DBBaseModel):
    __tablename__ = 'TB_PROJETO_FEDEX_HISTORICO'
    # "implicit_returning=false" não é recomendado. Usar somente se a tabela possuir Triggers(Gatilhos)
    __table_args__ = {'implicit_returning': False,
                      "extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    os: str = Column(String(250))
    callid: str = Column(String(250))
    ip: str = Column(String(250))


class RespTbProjetoModel(settings.DBBaseModel):
    __tablename__ = 'TB_PROJETO_FEDEX'
    # "implicit_returning=false" não é recomendado. Usar somente se a tabela possuir Triggers(Gatilhos)
    __table_args__ = {'implicit_returning': False,
                      "extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    call_id: str = Column(String(250), nullable=True)


class RespTbOperacionalModel(settings.DBBaseModel):
    __tablename__ = 'TB_FEDEX_OPERACIONAL'
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo: str = Column(String(50), nullable=True)
    conclusao_operador: str = Column(String(50), nullable=False)
    protocolo: bool = Column(Boolean, nullable=False)
