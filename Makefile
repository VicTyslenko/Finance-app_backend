.PHONY: help install dev migration migrate status clean

PORT ?= 8000

.DEFAULT_GOAL := help

# ── Help ────────────────────────────────────────────────────────────────────

help:
	@echo "Finance API"
	@echo ""
	@echo "Development:"
	@echo "  make install     uv sync — install dependencies"
	@echo "  make dev         Start the API with --reload (port $(PORT))"
	@echo "  make clean       Remove __pycache__ directories"
	@echo ""
	@echo "Database:"
	@echo "  make migration   Apply any unapplied database/*.sql"
	@echo "  make status      Show applied migrations and row counts"
	@echo ""
	@echo "Overrides:"
	@echo "  PORT=8001 make dev"

# ── Development ─────────────────────────────────────────────────────────────

install:
	uv sync

dev:
	uv run uvicorn api.main:app --reload --port $(PORT)

clean:
	find . -type d -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} +

# ── Database ────────────────────────────────────────────────────────────────

migration:
	uv run python scripts/migrate.py

# convenience alias
migrate: migration

status:
	uv run python scripts/db_status.py
