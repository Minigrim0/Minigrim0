#!/bin/bash

if [ $1 == "dev" ]; then
    DOCKERFILE=docker/docker-compose.dev.yml
    export COMPOSE_PROJECT_NAME="minigrim0-web-dev"
else
    DOCKERFILE=docker/docker-compose.yml
    export COMPOSE_PROJECT_NAME="minigrim0-web"
fi

docker-compose -f $DOCKERFILE up -d --build
docker-compose -f $DOCKERFILE exec web python manage.py makemigrations --noinput
docker-compose -f $DOCKERFILE exec web python manage.py migrate --noinput
docker-compose -f $DOCKERFILE exec web python manage.py collectstatic --noinput

if [ $1 != "dev" ]; then
    docker-compose -f $DOCKERFILE restart nginx
fi
