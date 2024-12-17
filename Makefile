.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000

export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up		# Stop, build and deploy all services

build:	# Assembling images
	docker compose build

up:		# Deploying all services and creating docker images
	docker compose up -d

down:	# Stop all services and remove containers
	docker compose down --remove-orphans

run:	# Run the application using uvicorn with provided arguments or defaults
	uvicorn src.main:app --host  $(HOST) --port $(PORT) --reload --env-file .env

migrate-create:		# Create a new revision migration
	alembic revision --autogenerate -m "$(MIGRATE)"

migrate-apply:		# Run migration
	alembic upgrade head

logs:
		docker compose logs --tail=25 worker

help:	# Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "  %-20s %s\n", $$1, $$2}'