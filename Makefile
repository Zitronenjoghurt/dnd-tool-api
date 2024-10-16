dev-up:
	docker compose -f docker-compose.dev.yml up --build

dev-down:
	docker compose -f docker-compose.dev.yml down

dev-restart: dev-down dev-up

prod-up:
	docker compose -f docker-compose.prod.yml up -d --build

prod-down:
	docker compose -f docker-compose.prod.yml down

prod-restart: prod-down prod-up

clean:
	docker compose -f docker-compose.dev.yml down -v --remove-orphans
	docker compose -f docker-compose.prod.yml down -v --remove-orphans

logs-dev:
	docker compose -f docker-compose.dev.yml logs -f

logs-prod:
	docker compose -f docker-compose.prod.yml logs -f
	docker compose up -d