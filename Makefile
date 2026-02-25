.PHONY: install test lint run-api

install:
	pip install -r requirements.txt

test:
	pytest services/core services/api

lint:
	black services
	flake8 services
	mypy services

run-api:
	uvicorn services.api.main:app --reload
