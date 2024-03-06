from sqlalchemy import Column, Integer, String, DateTime, Text
from core.configs import settings
from datetime import datetime


class RetencaoHistRespModel(settings.DBBaseModel):
    __tablename__ = 'TB_PROJETO_FEDEX_HISTORICO'
    # "implicit_returning=false" não é recomendado. Usar somente se a tabela possuir Triggers(Gatilhos)
    __table_args__ = {'implicit_returning': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    os: str = Column(String(250))
    callid: str = Column(String(250))
    ip: str = Column(String(250))

