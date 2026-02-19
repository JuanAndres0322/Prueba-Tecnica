import logging

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.voter import Voter
from app.models.candidate import Candidate
from app.models.vote import Vote
from app.schemas.vote import VoteCreate, VoteStatistics, CandidateStats

logger = logging.getLogger(__name__)


async def emitir_voto(db: AsyncSession, datos: VoteCreate) -> Vote:
    resultado = await db.execute(select(Voter).where(Voter.id == datos.voter_id))
    votante = resultado.scalar_one_or_none()
    if not votante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Votante no encontrado")

    resultado = await db.execute(select(Candidate).where(Candidate.id == datos.candidate_id))
    candidato = resultado.scalar_one_or_none()
    if not candidato:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidato no encontrado")

    if votante.has_voted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este votante ya emitió su voto")

    # todo en una sola transacción
    voto = Vote(voter_id=datos.voter_id, candidate_id=datos.candidate_id)
    votante.has_voted = True
    candidato.votes += 1

    db.add(voto)
    await db.commit()
    await db.refresh(voto)
    logger.info(f"Voto registrado: votante {datos.voter_id} -> candidato {datos.candidate_id}")
    return voto


async def listar_votos(db: AsyncSession) -> list[Vote]:
    resultado = await db.execute(select(Vote).order_by(Vote.id))
    return list(resultado.scalars().all())


async def obtener_estadisticas(db: AsyncSession) -> VoteStatistics:
    resultado = await db.execute(select(func.count(Vote.id)))
    total_votos = resultado.scalar() or 0

    resultado = await db.execute(
        select(func.count(Voter.id)).where(Voter.has_voted == True)
    )
    total_votantes = resultado.scalar() or 0

    resultado = await db.execute(select(Candidate).order_by(Candidate.votes.desc()))
    candidatos = resultado.scalars().all()

    stats = []
    for c in candidatos:
        pct = round((c.votes / total_votos * 100), 1) if total_votos > 0 else 0.0
        stats.append(CandidateStats(
            candidate_id=c.id,
            candidate_name=c.name,
            party=c.party,
            votes=c.votes,
            percentage=pct,
        ))

    return VoteStatistics(
        total_votes=total_votos,
        total_voters_voted=total_votantes,
        candidates=stats,
    )
