from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class VoterCreate(BaseModel):
    name: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()


class VoterResponse(BaseModel):
    id: int
    name: str
    email: str
    has_voted: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
