from pydantic import BaseModel as SCBaseModel


class MessageSchema(SCBaseModel):
    callid: str
    telefone: str
    os: str
    protocolo: str
    atendente: str
    codigo_conclusao: str
    obs: str

    class Config:
        from_attributes = True
