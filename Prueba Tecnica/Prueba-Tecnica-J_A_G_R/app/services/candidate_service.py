import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.candidate import Candidate
from app.models.voter import Voter
from app.schemas.candidate import CandidateCreate

logger = logging.getLogger(__name__)


async def crear_candidato(db: AsyncSession, datos: CandidateCreate) -> Candidate:
    # no puede tener el mismo nombre que un votante
    res = await db.execute(select(Voter).where(Voter.name == datos.name))
    if res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un votante registrado con ese nombre"
        )

    nuevo = Candidate(name=datos.name, party=datos.party)
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    logger.info(f"Candidato creado: {nuevo.id} - {nuevo.name}")
    return nuevo


async def listar_candidatos(db: AsyncSession) -> list[Candidate]:
    res = await db.execute(select(Candidate).order_by(Candidate.id))
    return list(res.scalars().all())


async def obtener_candidato(db: AsyncSession, candidato_id: int) -> Candidate:
    res = await db.execute(select(Candidate).where(Candidate.id == candidato_id))
    candidato = res.scalar_one_or_none()
    if not candidato:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidato no encontrado")
    return candidato


async def eliminar_candidato(db: AsyncSession, candidato_id: int) -> None:
    candidato = await obtener_candidato(db, candidato_id)
    if candidato.votes > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un candidato que ya tiene votos"
        )
    await db.delete(candidato)
    await db.commit()
    logger.info(f"Candidato eliminado: {candidato_id}")
