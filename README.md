# Blog Platform (Microservice Architecture)

Render URL: https://microservice-architecture-latest-oecc.onrender.com/

Render swagger URL: https://microservice-architecture-latest-oecc.onrender.com/docs#/

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

## Worker (Celery)

Асинхронный воркер на Celery + Redis для фоновых задач.

### Задача `notify_followers`

При создании статьи автоматически отправляет push-уведомления подписчикам автора:

- Читает подписчиков из таблицы `subscribers` (JOIN с `users` для `subscription_key`)
- Пропускает подписчиков без `subscription_key` (логирует warning)
- Проверяет идемпотентность через таблицу `notifications_sent`
- Retry с экспоненциальной задержкой (до 5 попыток), таймаут 5 секунд

### Настройка

```bash
cp worker/.env.example worker/.env
```

### Логи

```bash
docker compose --profile app logs -f worker
```

## API Gateway

- `/api/users/*` → users-service
- `/api/*` → backend

Health check: `GET /api/health`
