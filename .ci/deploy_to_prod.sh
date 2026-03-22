#!/bin/bash

set -e -o xtrace
# https://stackoverflow.com/a/5750463/7734535

export COMPOSE_PROJECT_NAME="git_notification_bot"

export prod_container_name="${COMPOSE_PROJECT_NAME}_app"
export prod_container_db_name="${COMPOSE_PROJECT_NAME}_db"
export docker_compose_file=".deploy/docker-compose.yml"
export prod_image_name_lower_case="${prod_container_name,,}"

docker rm -f "${prod_container_name}" || true

# 1. Capture the IDs into an array
# Using Docker's native filtering
mapfile -t images_to_delete < <(docker images -q --filter "reference=*${prod_image_name_lower_case}*")

# 2. Expand the array (properly quoted)
if [ ${#images_to_delete[@]} -gt 0 ]; then
    docker image rm -f "${images_to_delete[@]}" || true
fi

docker volume create --name="${COMPOSE_PROJECT_NAME}_logs"
docker compose -f "${docker_compose_file}" up -d

sleep 20

container_failed=$(docker ps -a -f "name=${prod_container_name}" --format "{{.Status}}" | head -1)
container_db_failed=$(docker ps -a -f "name=${prod_container_db_name}" --format "{{.Status}}" | head -1)


if [[ "${container_failed}" != *"Up"* ]]; then
    docker logs "${prod_container_name}"
    exit 1
fi

if [[ "${container_db_failed}" != *"Up"* ]]; then
    docker logs "${prod_container_db_name}"
    exit 1
fi
