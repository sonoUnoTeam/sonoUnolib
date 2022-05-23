IMAGE_NAME=${PWD##*/}
IMAGE_VERSION=$(poetry version --short)

docker build -t pchanial/${IMAGE_NAME}:${IMAGE_VERSION} .
