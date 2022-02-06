#!/bin/sh

if [ "$DATABASE" = "postgres" ]
  then
    echo "Waiting for psql"

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "Psql started"
fi

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py create_default_super_user
python manage.py runserver 0.0.0.0:8000

exec "$@"
