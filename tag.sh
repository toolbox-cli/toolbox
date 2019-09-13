NAME=$1
VERSION=$2
REPO_NAME=$3

for COMPONENT in `find ./components -mindepth 1 -type d | sort -u`
do
  [ -e $COMPONENT/Dockerfile ] || { echo "Dockerfile missing in '$COMPONENT' folder" && continue; }

  COMPONENT_NAME=`echo $COMPONENT | cut -d'/' -f3 | cut -d'/' -f1`

  `docker images --filter=reference="$REPO_NAME*:latest" | grep -sq "$COMPONENT_NAME" ` || \
      { echo "[!] Latest image is missing for '$COMPONENT_NAME'! Skipping..." && continue; }

  echo "Tagging '${REPO_NAME}_${COMPONENT_NAME}:latest' image as '$NAME/$COMPONENT_NAME:$VERSION'"
  docker tag ${REPO_NAME}_${COMPONENT_NAME}:latest $NAME/$COMPONENT_NAME:$VERSION
  docker tag $NAME/$COMPONENT_NAME:$VERSION $NAME/$COMPONENT_NAME:latest
done