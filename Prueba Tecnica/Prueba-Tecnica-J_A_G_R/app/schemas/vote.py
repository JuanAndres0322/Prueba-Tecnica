from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VoteCreate(BaseModel):
    voter_id: int
    candidate_id: int


class VoteResponse(BaseModel):
    id: int
    voter_id: int
    candidate_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CandidateStats(BaseModel):
    candidate_id: int
    candidate_name: str
    party: str | None
    votes: int
    percentage: float


class VoteStatistics(BaseModel):
    total_votes: int
    total_voters_voted: int
    candidates: list[CandidateStats]
