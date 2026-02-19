from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.vote import VoteCreate, VoteResponse, VoteStatistics
from app.services import vote_service

router = APIRouter(prefix="/votes", tags=["Votos"])


@router.post("/", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
async def emitir_voto(datos: VoteCreate, db: AsyncSession = Depends(get_db)):
    return await vote_service.emitir_voto(db, datos)


@router.get("/", response_model=list[VoteResponse])
async def listar_votos(db: AsyncSession = Depends(get_db)):
    return await vote_service.listar_votos(db)


@router.get("/statistics", response_model=VoteStatistics)
async def obtener_estadisticas(db: AsyncSession = Depends(get_db)):
    return await vote_service.obtener_estadisticas(db)
