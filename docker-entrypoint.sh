#!/bin/bash
set -e

COMMANDS="shell utils db sync runserver api match"

echo "Refreshing static files..."
STATIC_DIR="/var/local/art12/art12/static/"
TEMP_STATIC_DIR="/var/local/art12/temp_static/"
cp -a $TEMP_STATIC_DIR/. $STATIC_DIR
rm -r $TEMP_STATIC_DIR

if [ -z "$POSTGRES_ADDR" ]; then
  POSTGRES_ADDR="postgres"
fi

while ! nc -z $POSTGRES_ADDR 5432; do
  echo "Waiting for Postgres server at '$POSTGRES_ADDR' to accept connections on port 5432..."
  sleep 3s
done


if [ "x$MIGRATE" = 'xyes' ]; then
  echo "Running DB CMD: ./manage.py db upgrade"
  python -m flask db upgrade
fi

if [ -z "$1" ]; then
  echo "Serving on port 5000"
  exec gunicorn -e SCRIPT_NAME=$SCRIPT_NAME \
                manage:app \
                --name article12 \
                --bind 0.0.0.0:5000 \
                --access-logfile - \
                --error-logfile -
fi

if [[ $COMMANDS == *"$1"* ]]; then
  exec python -m flask "$@"
fi

exec "$@"
