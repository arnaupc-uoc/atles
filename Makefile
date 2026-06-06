include .env
export

.PHONY: build up stop dev logs

build:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml build

up:
	docker compose --env-file .env -f docker-compose.yml -f docker-compose.dev.yml up

seed:
	docker compose --env-file .env -f docker-compose.yml -f docker-compose.dev.yml run --rm backend python seed_data.py

down:
	docker compose --env-file .env -f docker-compose.yml -f docker-compose.dev.yml down

build-prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml build

up-prod:
	docker compose --env-file .env.production -f docker-compose.yml -f docker-compose.prod.yml up --build

down-prod:
	docker compose --env-file .env.production -f docker-compose.yml -f docker-compose.prod.yml down

