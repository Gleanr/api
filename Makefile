up:
	docker compose up

log_api:
	docker compose up -d && docker container logs -f gleanr-api

build:
	docker compose up --build

stop:
	docker compose stop

down:
	docker compose down

migrations:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Error: Please provide a migration message. Example: make migrations add user table"; \
		exit 1; \
	fi
	docker compose run api alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

migrations_apply:
	docker compose run api alembic upgrade head