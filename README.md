# Testing

Testing is a Django application for tests, assigned tasks, user profiles, and training result journals. The project is configured for MySQL in Docker and uses `uv` as the Python dependency manager.

## Stack

- Python 3.11
- Django 5.2
- MySQL 8.0
- Docker Compose
- uv

## Project Layout

```text
.
|-- build/
|   |-- Dockerfile
|   |-- docker-compose.yml
|   `-- entrypoint.sh
|-- config/             # Django project settings and urls
|-- initru/             # Main Django app
|-- manage.py
|-- pyproject.toml      # Python dependencies for uv
|-- requirements.txt    # Compatibility list for non-uv tools
`-- Makefile
```

## Quick Start With Docker

Start the app and MySQL:

```bash
make up
```

Open the application:

- App: http://localhost:8000
- Admin: http://localhost:8000/admin/

The web container waits for MySQL, applies migrations, collects static files, and starts Django automatically.

## Rebuild After Dependency Changes

When `pyproject.toml` changes, rebuild the web image:

```bash
make up-build
```

## Demo Users

Create one admin and one regular user:

```bash
make create-demo-users
```

Default credentials:

| Username | Password | Role |
| --- | --- | --- |
| `admin` | `admin12345` | Django admin / superuser |
| `user` | `user12345` | Regular user |

## Testing Seed Data

Load neutral demo data for the "Testing" theme:

```bash
make seed-test-data
```

The command starts Docker services if needed, applies migrations, and imports
`build/seed_testing.sql` into MySQL.

Seeded users all use the same password:

```text
test12345
```

| Username | Role |
| --- | --- |
| `admin_test` | Administrator / superuser |
| `responsible_test` | Responsible user / staff |
| `student_ivanov` | Student |
| `student_smirnova` | Student |
| `employee_petrov` | Employee |
| `employee_orlova` | Employee |

The seed creates neutral testing data: user roles, groups, the themes
`Информатика` and `Цифровая грамотность`, three available tests, and 10
informatics questions with answer options for each test.

## Make Commands

```bash
make up                 # Start containers in the background
make up-build           # Rebuild and start containers
make down               # Stop containers
make down-v             # Stop containers and remove MySQL volume
make restart            # Restart containers
make build              # Build images
make logs               # Follow all logs
make logs-web           # Follow Django logs
make logs-db            # Follow MySQL logs
make shell              # Open bash in the Django container
make db-shell           # Open MySQL CLI
make migrate            # Apply migrations
make makemigrations     # Create migrations
make createsuperuser    # Create a Django superuser interactively
make create-demo-users  # Create admin and regular demo user
make seed-test-data     # Load neutral testing demo data
make ps                 # Show container status
make clean              # Prune Docker cache
```

## Database

Docker Compose starts MySQL with these development defaults:

```text
Database: briefing
User: briefing_user
Password: briefing_pass
Host from Django container: db
Host port: 3307
Container port: 3306
```

Django reads database settings from environment variables:

```text
DB_ENGINE=django.db.backends.mysql
DB_NAME=briefing
DB_USER=briefing_user
DB_PASSWORD=briefing_pass
DB_HOST=db
DB_PORT=3306
```

If these variables are not set, local Django falls back to `db.sqlite3`.

## Local Development With uv

Install uv first if it is not installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Create a virtual environment and install dependencies:

```bash
uv sync
```

Run Django locally with SQLite fallback:

```bash
uv run python manage.py migrate
uv run python manage.py runserver
```

To use local MySQL instead, export the same `DB_*` variables used by Docker Compose.

## Code Style

Ruff is configured in `pyproject.toml` and installed as a uv dev dependency.

```bash
make ruff-check
make ruff-fix
make ruff-format
```

## Useful Checks

Check Django configuration inside the running container:

```bash
docker compose -f build/docker-compose.yml exec -T web python manage.py check
```

Check that Django is using MySQL:

```bash
docker compose -f build/docker-compose.yml exec -T web python manage.py shell
```

Then run:

```python
from django.db import connection

print(connection.vendor)
print(connection.settings_dict["ENGINE"])
```

Expected output:

```text
mysql
django.db.backends.mysql
```

## Notes

- `pyproject.toml` is now the canonical dependency file.
- `requirements.txt` is kept only for compatibility with old tooling.
- `db.sqlite3` is not used by Docker Compose because Docker sets MySQL environment variables.
- `make down-v` deletes the MySQL volume and all container database data.
