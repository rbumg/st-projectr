PORT ?= 8000

.PHONY: help db.makemigrations db.migrate db.seed debug install format lint shell shell_plus test

db.makemigrations:
	python manage.py makemigrations

db.migrate:
	python manage.py migrate

db.seed:
	python manage.py seed

db.setup: db.makemigrations db.migrate db.seed

debug:
	python manage.py runserver_plus 0.0.0.0:$(PORT)

init: db.setup
	cp .env.example .env && echo "Please fill in the .env file"

install:
	poetry install

format:
	poetry run ruff format .

lint:
	poetry run ruff lint .

shell:
	poetry shell

shell_plus:
	python manage.py shell_plus

test:
	python manage.py test