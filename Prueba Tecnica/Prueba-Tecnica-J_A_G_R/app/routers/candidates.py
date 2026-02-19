from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.services import candidate_service

router = APIRouter(prefix="/candidates", tags=["Candidatos"])


@router.post("/", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def crear_candidato(datos: CandidateCreate, db: AsyncSession = Depends(get_db)):
    return await candidate_service.crear_candidato(db, datos)


@router.get("/", response_model=list[CandidateResponse])
async def listar_candidatos(db: AsyncSession = Depends(get_db)):
    return await candidate_service.listar_candidatos(db)


@router.get("/{candidato_id}", response_model=CandidateResponse)
async def obtener_candidato(candidato_id: int, db: AsyncSession = Depends(get_db)):
    return await candidate_service.obtener_candidato(db, candidato_id)


@router.delete("/{candidato_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_candidato(candidato_id: int, db: AsyncSession = Depends(get_db)):
    await candidate_service.eliminar_candidato(db, candidato_id)
