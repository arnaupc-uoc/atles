include .env
export

.PHONY: build up stop dev logs

build:
	docker compose --env-file .env build

up:
	docker compose --env-file .env up -d

stop:
	docker compose --env-file .env down

dev:
	docker compose --env-file .env up

logs:
	docker compose --env-file .env logs -f
