import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.voter import Voter
from app.models.candidate import Candidate
from app.schemas.voter import VoterCreate

logger = logging.getLogger(__name__)


async def crear_votante(db: AsyncSession, datos: VoterCreate) -> Voter:
    # email único
    existente = await db.execute(select(Voter).where(Voter.email == datos.email))
    if existente.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un votante con ese email"
        )

    # que no sea un candidato existente
    candidato = await db.execute(select(Candidate).where(Candidate.name == datos.name))
    if candidato.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un candidato con ese nombre"
        )

    nuevo = Voter(name=datos.name, email=datos.email)
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    logger.info(f"Votante creado: {nuevo.id} - {nuevo.name}")
    return nuevo


async def listar_votantes(db: AsyncSession) -> list[Voter]:
    resultado = await db.execute(select(Voter).order_by(Voter.id))
    return list(resultado.scalars().all())


async def obtener_votante(db: AsyncSession, votante_id: int) -> Voter:
    resultado = await db.execute(select(Voter).where(Voter.id == votante_id))
    votante = resultado.scalar_one_or_none()
    if not votante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Votante no encontrado")
    return votante


async def eliminar_votante(db: AsyncSession, votante_id: int) -> None:
    votante = await obtener_votante(db, votante_id)
    if votante.has_voted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un votante que ya emitió su voto"
        )
    await db.delete(votante)
    await db.commit()
    logger.info(f"Votante eliminado: {votante_id}")
