#!/bin/bash

# Required for docker-compose to use buildkit
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

help_text () {
    echo "Usage: $0 {build|attach|logs} {dev|prod}"
    exit 1
}

get_docker_file () {
    case $1 in
        dev)
            DOCKERFILE="docker/docker-compose.dev.yml"
            export COMPOSE_PROJECT_NAME="minigrim0-web-dev"
            ;;
        prod)
            DOCKERFILE="docker/docker-compose.yml"
            export COMPOSE_PROJECT_NAME="minigrim0-web"
            ;;
        *)
            help_text
            ;;
    esac
}

case $1 in
    build)
        get_docker_file $2

        docker-compose -f $DOCKERFILE up -d --build
        docker-compose -f $DOCKERFILE exec web python manage.py makemigrations --noinput
        docker-compose -f $DOCKERFILE exec web python manage.py migrate --noinput
        docker-compose -f $DOCKERFILE exec web python manage.py collectstatic --noinput

        if [ $2 != "dev" ]; then  # nginx is not in dev
            docker-compose -f $DOCKERFILE restart nginx
        fi
        ;;
    attach)
        get_docker_file $2  # $2 is dev or prod
        docker-compose -f $DOCKERFILE exec web bash  # bash is the default
        exit 0
        ;;
    logs)
        get_docker_file $2  # $2 is dev or prod
        docker-compose -f $DOCKERFILE logs -f web  # -f is for follow
        exit 0
        ;;
    *)
        echo "Usage: $0 {build|attach|logs} {dev|prod}"
        exit 1
esac
