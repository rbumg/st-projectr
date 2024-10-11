PORT ?= 8000

.PHONY: help db.makemigrations db.migrate db.seed debug docker.build docker.run docker.loadprojects install format lint shell shell_plus test

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

docker.run:
	docker-compose up -d

docker.loadprojects:
	docker-compose exec web python manage.py loaddata projects_fixture.json

init: db.setup
	cp .env.example .env && echo "Please fill in the .env file"

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
