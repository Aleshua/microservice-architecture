# Blog Platform (Microservice Architecture)

FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL

## Quick start

```bash
# full stack (app + db)
docker compose --profile app up --build

# only database for local development
docker compose --profile dev up
```

## Local development

```bash
cp .env.example .env
docker compose --profile dev up -d  # start postgres
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Migrations

```bash
# apply all migrations
docker compose --profile app exec app alembic upgrade head

# rollback last migration
docker compose --profile app exec app alembic downgrade -1

# auto-generate new migration
docker compose --profile app exec app alembic revision --autogenerate -m "migration_name"
```

Health check: `GET /api/health` → `{"status": "ok"}`
