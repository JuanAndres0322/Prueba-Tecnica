# Sistema de Votaciones API

API REST para manejar un sistema de votaciones: registrar votantes, candidatos y emitir votos.

## Cómo correr el proyecto

Necesitás Python 3.11+, Docker y pip.

```bash
# clonar y entrar al proyecto
git clone <url-del-repo>
cd voting-system

# entorno virtual
python -m venv venv
source venv/bin/activate  # en windows: venv\Scripts\activate
pip install -r requirements.txt

# levantar postgres
docker-compose up -d

# copiar variables de entorno (los defaults ya coinciden con el docker-compose)
cp .env.example .env

# migraciones
alembic upgrade head

# arrancar el server
uvicorn app.main:app --reload
```

Queda corriendo en `http://localhost:8000`. La doc de Swagger está en `/docs` y ReDoc en `/redoc`.

## Estructura del proyecto

```
voting-system/
├── app/
│   ├── main.py          # app de FastAPI, CORS, routers
│   ├── config.py        # variables de entorno
│   ├── database.py      # conexión async a postgres
│   ├── models/          # tablas
│   ├── schemas/         # validación de datos
│   ├── routers/         # endpoints
│   └── services/        # lógica de negocio
├── alembic/             # migraciones
├── docker-compose.yml
└── requirements.txt
```

Los routers reciben el request, los services manejan la lógica, los models definen las tablas. Nada raro.

## Endpoints

### Votantes

```bash
# crear votante
curl -X POST http://localhost:8000/api/v1/voters/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Carlos García", "email": "carlos@mail.com"}'

# listar todos
curl http://localhost:8000/api/v1/voters/

# obtener por id
curl http://localhost:8000/api/v1/voters/1

# eliminar (no deja si ya votó)
curl -X DELETE http://localhost:8000/api/v1/voters/2
```

### Candidatos

```bash
# crear candidato
curl -X POST http://localhost:8000/api/v1/candidates/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Juan Pérez", "party": "Partido A"}'

# listar todos
curl http://localhost:8000/api/v1/candidates/

# obtener por id
curl http://localhost:8000/api/v1/candidates/1

# eliminar (no deja si tiene votos)
curl -X DELETE http://localhost:8000/api/v1/candidates/2
```

### Votos

```bash
# votar
curl -X POST http://localhost:8000/api/v1/votes/ \
  -H "Content-Type: application/json" \
  -d '{"voter_id": 1, "candidate_id": 1}'

# listar votos
curl http://localhost:8000/api/v1/votes/

# estadísticas
curl http://localhost:8000/api/v1/votes/statistics
```

Ejemplo de respuesta de estadísticas:

```json
{
  "total_votes": 1,
  "total_voters_voted": 1,
  "candidates": [
    {
      "candidate_id": 1,
      "candidate_name": "Juan Pérez",
      "party": "Partido A",
      "votes": 1,
      "percentage": 100.0
    }
  ]
}
```

Si un votante intenta votar dos veces devuelve 400:

```json
{"detail": "Este votante ya emitió su voto"}
```

## Modelo de datos

```
+--------------+         +--------------+         +--------------+
|   voters     |         |    votes     |         |  candidates  |
+--------------+         +--------------+         +--------------+
| id (PK)      |----+    | id (PK)      |    +---| id (PK)      |
| name         |    +--->| voter_id (FK)|    |   | name         |
| email (UK)   |         | candidate_id |----+   | party        |
| has_voted    |         | created_at   |        | votes        |
| created_at   |         +--------------+        | created_at   |
+--------------+                                 +--------------+

- Un votante puede emitir máximo 1 voto
- Un candidato puede recibir muchos votos
```

## Stack

- Python 3.11+
- FastAPI 0.115.6
- SQLAlchemy 2.0.36 (async con asyncpg 0.30.0)
- Alembic 1.14.1
- Pydantic 2.10.4
- PostgreSQL 16
- Docker para la BD
