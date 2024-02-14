'''
Esse arquivo deve ser alterado e salvo como "configs.py"
'''
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


class Settings(BaseSettings):
    '''
    Congigurações gerais da API
    '''
    API_V1_STR: str = '/api/v1'
    # DB_URL: str = "mssql+aioodbc://fastapi:Profeta#2@DB-03:1433/teste?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    DB_URL: str = "mssql+aioodbc://USUARIO:SENHA@IP_OU_NOME_SERVIDOR:PORTA/NOME_DB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    DBBaseModel: DeclarativeMeta = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
