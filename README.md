# Minimal Django + Postgres + Redis + Celery (Docker)

## Quickstart

1. Create an `.env` based on the example below. You can also set these via your CI/host.
2. Build and start services:

```bash
docker compose up --build
```

- Web: http://localhost:8000
- Health check: http://localhost:8000/health (queues a `ping` Celery task)

## Environment variables

These are read by Django/Celery and the Postgres container.

```env
# Django
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=1
ALLOWED_HOSTS=*

# Postgres
POSTGRES_DB=exampledb
POSTGRES_USER=exampleuser
POSTGRES_PASSWORD=examplepass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Timezone
TZ=UTC
```

## Notes
- `docker-compose.yml` starts `web` (Django), `worker` (Celery), `db` (Postgres), and `redis`.
- `web` runs migrations automatically on startup, then serves on `0.0.0.0:8000`.
- The `health` endpoint enqueues a `ping` task so you can verify worker wiring.
