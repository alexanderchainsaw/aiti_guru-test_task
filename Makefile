lint:
	uv run isort ./app
	uv run black ./app
	uv run ruff check ./app

reqs:
	uv pip freeze > requirements.txt


dev-start:
	docker-compose -f deployments/docker-compose.dev.yml up -d --force-recreate

dev-stop:
	docker-compose -f deployments/docker-compose.dev.yml down

dev-build:
	docker-compose -f deployments/docker-compose.dev.yml build --no-cache

dev-run: dev-stop dev-build dev-start