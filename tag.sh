REPO_NAME=$1
VERSION=$2
COMPOSE_PREFIX=`basename $(dirname $(realpath $0))`

for COMPONENT in `find ./cli-command-images -mindepth 1 -type d | sort -u`
do
  # Dockerfile is missing, therefore not a docker image directory.
  [ -e $COMPONENT/Dockerfile ] || { continue; }

  COMPONENT_NAME=`basename $COMPONENT`
  COMPONENT_TYPE=$(basename `dirname $COMPONENT`)

  `docker images --filter=reference="$COMPOSE_PREFIX*$COMPONENT_NAME*:latest" | grep -sq "$COMPONENT_NAME" ` || \
  { echo "[!] Latest image is missing for '$COMPONENT_NAME'! Skipping..." && continue; }

  echo "Tagging '${COMPOSE_PREFIX}_${COMPONENT_NAME}:latest' image as '$REPO_NAME:${COMPONENT_TYPE}_${COMPONENT_NAME}_$VERSION'"
  docker tag ${COMPOSE_PREFIX}_${COMPONENT_NAME}:latest ${COMPONENT_TYPE}_${COMPONENT_NAME}_$VERSION || exit 1
  docker tag ${COMPONENT_TYPE}_${COMPONENT_NAME}_$VERSION $REPO_NAME:${COMPONENT_TYPE}_${COMPONENT_NAME}_$VERSION || exit 2
done