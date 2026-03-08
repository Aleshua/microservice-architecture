# Blog Platform (Microservice Architecture)

FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL + Nginx API Gateway

## Quick start

```bash
cp .env.example .env
docker compose --profile app up --build
```

## Migrations

### Users Service

```bash
docker compose --profile app exec users-service alembic upgrade head
docker compose --profile app exec users-service alembic downgrade -1
docker compose --profile app exec users-service alembic revision --autogenerate -m "migration_name"
```

### Backend

```bash
docker compose --profile app exec backend alembic upgrade head
docker compose --profile app exec backend alembic downgrade -1
docker compose --profile app exec backend alembic revision --autogenerate -m "migration_name"
```

## API Gateway

- `/api/users/*` → users-service
- `/api/*` → backend

Health check: `GET /api/health`
