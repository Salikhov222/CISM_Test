.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000

export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up migrations 		# Stop, build and deploy all services

build:	# Assembling images
	docker compose build

up:		# Deploying all services and creating docker images
	docker compose up -d

down:	# Stop all services and remove containers
	docker compose down --remove-orphans

run:	# Run the application using uvicorn with provided arguments or defaults
	uvicorn src.main:app --host  $(HOST) --port $(PORT) --reload --env-file .env

test: up	# Run unit tests
	docker compose run --rm --no-deps --entrypoint=pytest app /tests/unit

migrations:		# Create a new revision migration and run migration
	alembic revision --autogenerate -m "initial"
	alembic upgrade head

logs-worker:	# Show log app service
	docker compose logs --tail=25 worker

logs-app:		# Show logs worker service
	docker compose logs --tail=25 app

help:	# Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "  %-20s %s\n", $$1, $$2}'