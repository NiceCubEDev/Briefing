#!/bin/bash
set -e

echo "Ожидание готовности MySQL..."
while ! nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null; do
    sleep 1
done
echo "MySQL готов!"

echo "Применение миграций..."
python manage.py migrate --noinput

echo "Сбор статики..."
python manage.py collectstatic --noinput 2>/dev/null || true

exec "$@"
