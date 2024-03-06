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

router = APIRouter()

api_versao = 'api/V1'
