from sqlalchemy import Column, Integer, String, DateTime, Text
from core.configs import settings


class ProjetoBase(settings.DBBaseModel):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    PROJETO = Column(String(250))
    Cliente = Column(String(6))


class ProjetoFdModel(ProjetoBase):
    __tablename__ = 'TB_PROJETO'


class ProjetoCtbseqModel(ProjetoBase):
    __tablename__ = 'TB_PROJETO_CTBSEQ'


class OcorrenciasModel(settings.DBBaseModel):
    __tablename__ = 'Motivos_fedex'
    motivo: str = Column(String(250))
    id = Column(Integer, primary_key=True, autoincrement=True)
    projeto: str = Column(String(250))


class TiposModel(settings.DBBaseModel):
    __tablename__ = 'TB_TIPO_ATENDIMENTO'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Tipo_Atendimento: str = Column(String(250))


class RetencaoAbModel(settings.DBBaseModel):
    __tablename__ = 'TB_PROJETO_FEDEX'
    __table_args__ = {'implicit_returning': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    dt_abertura = Column(DateTime)
    atendente_abertura: str = Column(String(250), nullable=True)
    retorno_tecnico: str = Column(String(250), nullable=True)
    nome_tecnico: str = Column(String(250), nullable=True)
    telefone_tecnico: str = Column(String(250), nullable=True)
    os: str = Column(String(250))
    problema_apresentado: str = Column(Text, nullable=True)
    ocorrencia: str = Column(String(250), nullable=True)
    acao_D29: str = Column(String(250), nullable=True)
    projeto: str = Column(String(250), nullable=True)
    tipo_atendimento: str = Column(String(250), nullable=True)
    status: str = Column(String(250), nullable=True)
    subprojeto: str = Column(String(250), nullable=True)
    cliente: str = Column(String(250), nullable=True)
    versao: str = Column(String(250), nullable=True)
    chave: str = Column(String(250), nullable=True)
    dt_fechamento = Column(DateTime, nullable=True)
    fase: str = Column(String(250), nullable=True)
    conclusao_operador: str = Column(String(250), nullable=True)
    definicao: str = Column(String(250), nullable=True)
    status_relatorio: str = Column(String(250), nullable=True)
    etapa: str = Column(String(250), nullable=True)
    tipo: str = Column(String(250), nullable=True)
    acao_d1: str = Column(String(250), nullable=True)
