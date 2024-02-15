'''
Esse arquivo deve ser alterado e salvo como "configs.py"
'''
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


class Settings(BaseSettings):
    '''
    Congigurações gerais da API
    '''
    API_V1_STR: str = '/Retencao/api/v1'
    DB_URL: str = "mssql+aioodbc://USUARIO:SENHA@IP_OU_NOME_SERVIDOR:PORTA/NOME_DB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    DBBaseModel: DeclarativeMeta = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
