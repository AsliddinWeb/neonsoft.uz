DC = docker compose --env-file .env
DC_PROD = docker compose --env-file .env -f docker-compose.prod.yml

# ─── Dev ───────────────────────────────────────────
up:
	$(DC) up --build

down:
	$(DC) down

restart:
	$(DC) restart

logs:
	$(DC) logs -f

logs-api:
	$(DC) logs -f api

logs-front:
	$(DC) logs -f frontend

# ─── Database ──────────────────────────────────────
migrate:
	$(DC) exec api alembic upgrade head

makemigrations:
	$(DC) exec api alembic revision --autogenerate -m "$(msg)"

seed:
	$(DC) exec api python seed.py

# ─── Utils ─────────────────────────────────────────
shell-api:
	$(DC) exec api bash

shell-front:
	$(DC) exec frontend sh

shell-db:
	$(DC) exec db psql -U neonsoft -d neonsoft_db

# ─── Production ───────────────────────────────────
prod-up:
	$(DC_PROD) up --build -d

prod-down:
	$(DC_PROD) down

prod-restart:
	$(DC_PROD) restart

prod-logs:
	$(DC_PROD) logs -f

prod-migrate:
	$(DC_PROD) exec api alembic upgrade head

prod-seed:
	$(DC_PROD) exec api python seed.py
