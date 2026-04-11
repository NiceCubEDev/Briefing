DC = docker compose
DC_FILE = build/docker-compose.yml
UV ?= $(HOME)/.local/bin/uv
UVX ?= $(HOME)/.local/bin/uvx

.PHONY: up down restart build logs shell db-shell migrate makemigrations createsuperuser create-demo-users uv-sync uv-lock uv-check uv-runserver ruff-check ruff-fix ruff-format ps clean help

## Запустить все сервисы (в фоне)
up:
	$(DC) -f $(DC_FILE) up -d

## Запустить с пересборкой образов
up-build:
	$(DC) -f $(DC_FILE) up -d --build

## Остановить все сервисы
down:
	$(DC) -f $(DC_FILE) down

## Остановить и удалить volumes (полный сброс БД!)
down-v:
	$(DC) -f $(DC_FILE) down -v

## Перезапустить все сервисы
restart:
	$(DC) -f $(DC_FILE) restart

## Пересобрать образы без запуска
build:
	$(DC) -f $(DC_FILE) build

## Показать логи всех сервисов (live)
logs:
	$(DC) -f $(DC_FILE) logs -f

## Показать логи только Django
logs-web:
	$(DC) -f $(DC_FILE) logs -f web

## Показать логи только MySQL
logs-db:
	$(DC) -f $(DC_FILE) logs -f db

## Открыть bash внутри контейнера Django
shell:
	$(DC) -f $(DC_FILE) exec web bash

## Открыть MySQL CLI внутри контейнера БД
db-shell:
	docker exec -it briefing_db mysql -u briefing_user -pbriefing_pass briefing

## Применить миграции
migrate:
	$(DC) -f $(DC_FILE) exec web python manage.py migrate

## Создать новые миграции из моделей
makemigrations:
	$(DC) -f $(DC_FILE) exec web python manage.py makemigrations

## Создать суперпользователя Django
createsuperuser:
	$(DC) -f $(DC_FILE) exec web python manage.py createsuperuser

## Create two demo users: one admin and one regular user
create-demo-users:
	$(DC) -f $(DC_FILE) exec web python manage.py create_demo_users

## Install/update local dependencies with uv
uv-sync:
	$(UV) sync

## Generate/update uv.lock
uv-lock:
	$(UV) lock

## Run Django system check through uv
uv-check:
	$(UV) run python manage.py check

## Run local Django development server through uv
uv-runserver:
	$(UV) run python manage.py runserver

## Run Ruff lint check
ruff-check:
	$(UVX) ruff check .

## Run Ruff lint with autofix
ruff-fix:
	$(UVX) ruff check . --fix --exit-zero

## Format Python files with Ruff
ruff-format:
	$(UVX) ruff format .

## Показать статус контейнеров
ps:
	$(DC) -f $(DC_FILE) ps

## Удалить остановленные контейнеры, лишние images и volumes
clean:
	docker system prune -f

## Показать все доступные команды
help:
	@echo ""
	@echo "  Briefing — доступные команды Make:"
	@echo ""
	@echo "  make up              — запустить сервисы в фоне"
	@echo "  make up-build        — пересобрать и запустить"
	@echo "  make down            — остановить сервисы"
	@echo "  make down-v          — остановить + удалить БД (volume)"
	@echo "  make restart         — перезапустить сервисы"
	@echo "  make build           — пересобрать образы"
	@echo "  make logs            — логи всех сервисов"
	@echo "  make logs-web        — логи Django"
	@echo "  make logs-db         — логи MySQL"
	@echo "  make shell           - bash inside Django container"
	@echo "  make db-shell        - MySQL CLI inside DB container"
	@echo "  make migrate         — применить миграции"
	@echo "  make makemigrations  — создать новые миграции"
	@echo "  make createsuperuser — создать суперпользователя"
	@echo "  make create-demo-users - create admin and user"
	@echo "  make uv-sync          - install dependencies with uv"
	@echo "  make uv-lock          - generate or update uv.lock"
	@echo "  make uv-check         - run Django check through uv"
	@echo "  make uv-runserver     - run local Django server through uv"
	@echo "  make ruff-check       - run Ruff lint"
	@echo "  make ruff-fix         - run Ruff lint with autofix"
	@echo "  make ruff-format      - format Python files with Ruff"
	@echo "  make ps              — статус контейнеров"
	@echo "  make clean           — очистить Docker мусор"
	@echo ""
