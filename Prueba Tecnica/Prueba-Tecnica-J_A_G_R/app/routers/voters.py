from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.voter import VoterCreate, VoterResponse
from app.services import voter_service

router = APIRouter(prefix="/voters", tags=["Votantes"])


@router.post("/", response_model=VoterResponse, status_code=status.HTTP_201_CREATED)
async def crear_votante(datos: VoterCreate, db: AsyncSession = Depends(get_db)):
    return await voter_service.crear_votante(db, datos)


@router.get("/", response_model=list[VoterResponse])
async def listar_votantes(db: AsyncSession = Depends(get_db)):
    return await voter_service.listar_votantes(db)


@router.get("/{votante_id}", response_model=VoterResponse)
async def obtener_votante(votante_id: int, db: AsyncSession = Depends(get_db)):
    return await voter_service.obtener_votante(db, votante_id)


@router.delete("/{votante_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_votante(votante_id: int, db: AsyncSession = Depends(get_db)):
    await voter_service.eliminar_votante(db, votante_id)
