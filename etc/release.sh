#!/bin/bash
#
# Release the current version of arcadia mock, as follows:
# - Fetch the version number from the Python package
# - Add a tag to the git hub repository
# - Build the associated docker image
# - Push the docker image

NAME="fchauvel/arcadia-mock"
DOCKERFILE="./etc/Dockerfile"

# Fetch the version number
source ./venv/Scripts/activate
export COVERAGE_PROCESS_START=".coveragerc"
VERSION=$(python -c "import arcadiamock; print arcadiamock.__VERSION__" | grep -Po "\d.\d.\d")

# Run the test
python setup.py test

# Create a tag and push it
git tag -a v$VERSION -m "Release $VERSION"
git push origin v$VERSION

# Build a new docker image
echo $DOCKERFILE
docker build -f $DOCKERFILE -t $NAME --build-arg version=$VERSION .
docker tag $NAME $NAME:v$VERSION
docker tag $NAME $NAME:latest
docker push $NAME

echo "Version $VERSION released."
