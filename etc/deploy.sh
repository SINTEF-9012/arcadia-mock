#!/bin/bash
# ssh -i key ec2-user@34.250.221.100 'bash -s' < deploy.sh

IMAGE=fchauvel/arcadia-mock
APP=arcadia-mock

docker pull $IMAGE:latest
docker stop $APP
docker rm $APP
docker rmi $IMAGE:current
docker tag $IMAGE:latest $IMAGE:current
docker run -d -p 80:1234 --name $APP $IMAGE:latest
