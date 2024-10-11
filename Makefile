PORT ?= 8000

.PHONY: help db.makemigrations db.migrate db.seed db.setup debug docker.build docker.loadprojects docker.logs docker.run docker.stop install format lint loadprojects shell shell_plus test

db.makemigrations:
	python manage.py makemigrations

db.migrate:
	python manage.py migrate

db.seed:
	python manage.py seed

db.setup: db.makemigrations db.migrate db.seed

debug:
	python manage.py runserver_plus 0.0.0.0:$(PORT)

docker.build:
	docker-compose build

docker.loadprojects:
	docker-compose exec web python manage.py loaddata projects_fixture.json

docker.logs:
	docker-compose logs -f

docker.run:
	docker-compose up -d

docker.stop:
	docker-compose down

init: db.setup
	@if [ ! -f .env ]; then cp .env.example .env && echo "Please fill in the .env file"; else echo ".env file already exists"; fi

install:
	poetry install

format:
	poetry run ruff format .

lint:
	poetry run ruff lint .

loadprojects:
	python manage.py loaddata projects_fixture.json

shell:
	poetry shell

shell_plus:
	python manage.py shell_plus

test:
	poetry run pytest --cov=app --cov-report=term-missing --cov-report=html
