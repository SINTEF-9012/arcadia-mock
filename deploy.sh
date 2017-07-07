#!/bin/bash

IMAGE=vassik/arcadia-mock:latest
APP=arcadia-mock

docker stop $APP
docker rm $APP
docker rmi -f $IMAGE
docker build --no-cache=true --rm -t $IMAGE .
docker run -d -p 80:1234 --name $APP $IMAGE
docker logs -f $APP
