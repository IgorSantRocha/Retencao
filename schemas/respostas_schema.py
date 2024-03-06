from typing import Optional
from datetime import datetime

from pydantic import BaseModel as SCBaseModel


class MessageSchema(SCBaseModel):
    callid: str
    os: str
    atendente: str
    conclusao: str
    obs: str
    telefone: str

    class Config:
        from_attributes = True
