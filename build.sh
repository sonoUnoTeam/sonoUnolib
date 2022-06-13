set -ex

IMAGE_NAME=pchanial/${PWD##*/}
IMAGE_VERSION=$(poetry version --short)

docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .
docker tag ${IMAGE_NAME}:${IMAGE_VERSION} ${IMAGE_NAME}:latest
