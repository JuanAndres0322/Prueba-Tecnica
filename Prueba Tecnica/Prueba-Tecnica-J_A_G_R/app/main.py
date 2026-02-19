import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import voters, candidates, votes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Sistema de Votaciones",
    description="API para gestionar votantes, candidatos y votos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voters.router, prefix="/api/v1")
app.include_router(candidates.router, prefix="/api/v1")
app.include_router(votes.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"mensaje": "Sistema de Votaciones API v1.0"}
