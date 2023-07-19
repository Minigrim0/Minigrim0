DOCKERFILE=docker/docker-compose.yml
export COMPOSE_PROJECT_NAME="minigrim0-web"
docker-compose -f $DOCKERFILE up -d --build
