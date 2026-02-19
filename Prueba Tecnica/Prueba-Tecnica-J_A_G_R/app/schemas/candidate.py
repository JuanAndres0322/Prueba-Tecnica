from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class CandidateCreate(BaseModel):
    name: str
    party: str | None = None

    @field_validator("name")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()


class CandidateResponse(BaseModel):
    id: int
    name: str
    party: str | None
    votes: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
