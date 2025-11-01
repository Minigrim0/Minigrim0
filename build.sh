#!/usr/bin/env bash

# Required for docker-compose to use buildkit
export DOCKER_BUILDKIT=1
export COMPOSE_BAKE=true
export COMPOSE_DOCKER_CLI_BUILD=1

help_text () {
    echo "Usage: $0 {up|deploy|attach|logs|down} {dev|prod}"
    echo "  up     - Start with docker compose (local development)"
    echo "  deploy - Deploy to docker swarm (production only)"
    echo "  attach - Attach to web container"
    echo "  logs   - Follow web container logs"
    echo "  down   - Stop containers"
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
    up)
        get_docker_file $2

        docker compose -f $DOCKERFILE up -d --build \
            || { echo "docker compose up failed"; exit 1; }

        docker compose -f $DOCKERFILE exec web uv run manage.py makemigrations --noinput \
            || { echo "makemigrations failed"; exit 1; }
        docker compose -f $DOCKERFILE exec web uv run manage.py migrate --noinput \
            || { echo "migrate failed"; exit 1; }
        docker compose -f $DOCKERFILE exec web uv run manage.py collectstatic --noinput \
            || { echo "collectstatic failed"; exit 1; }

        if [ $2 != "dev" ]; then  # nginx is not in dev
            docker compose -f $DOCKERFILE restart nginx
        fi
        ;;
    deploy)
        get_docker_file $2

        if [ $2 != "prod" ]; then
            echo "Error: deploy only works with prod environment"
            exit 1
        fi

        echo "Building images..."
        docker compose -f $DOCKERFILE build \
            || { echo "docker compose build failed"; exit 1; }

        echo "Deploying stack to swarm..."
        docker stack deploy --with-registry-auth -c $DOCKERFILE $COMPOSE_PROJECT_NAME \
            || { echo "docker stack deploy failed"; exit 1; }

        echo "Stack deployed successfully!"
        echo ""
        echo "Waiting 15 seconds for services to start..."
        sleep 15

        # Run migrations on web service
        SERVICE_NAME="${COMPOSE_PROJECT_NAME}_web"
        echo "Running database migrations..."

        # Get the task ID for the web service
        TASK_ID=$(docker service ps --filter "desired-state=running" $SERVICE_NAME -q | head -1)

        if [ -z "$TASK_ID" ]; then
            echo "Warning: Could not find running web service."
            echo "Please run migrations manually after services are up:"
            echo "  docker exec \$(docker ps -q -f name=${SERVICE_NAME}) uv run manage.py migrate"
        else
            # Get container ID from task
            CONTAINER_ID=$(docker inspect --format '{{.Status.ContainerStatus.ContainerID}}' $TASK_ID)

            if [ -z "$CONTAINER_ID" ]; then
                echo "Warning: Could not find web container."
                echo "Please run migrations manually:"
                echo "  docker exec \$(docker ps -q -f name=${SERVICE_NAME}) uv run manage.py migrate"
            else
                echo "Running migrations in container $CONTAINER_ID..."
                docker exec $CONTAINER_ID uv run manage.py makemigrations --noinput || true
                docker exec $CONTAINER_ID uv run manage.py migrate --noinput || echo "Migration failed"
                docker exec $CONTAINER_ID uv run manage.py collectstatic --noinput || echo "Collectstatic failed"
            fi
        fi

        echo ""
        echo "Deployment complete!"
        echo "Check service status with: docker service ls"
        echo "Check logs with: docker service logs ${SERVICE_NAME}"
        ;;
    restart)
        get_docker_file $2
        docker compose -f $DOCKERFILE restart
        ;;
    attach)
        get_docker_file $2  # $2 is dev or prod
        docker compose -f $DOCKERFILE exec web bash  # bash is the default
        ;;
    logs)
        get_docker_file $2  # $2 is dev or prod
        docker compose -f $DOCKERFILE logs -f web  # -f is for follow
        ;;
    down)
        get_docker_file $2  # $2 is dev or prod
        docker compose -f $DOCKERFILE down
        ;;
    *)
        help_text
esac

exit 0
