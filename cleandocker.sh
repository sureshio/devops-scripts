#!/bin/bash

docker rmi $(docker images -aq --filter dangling=true)

# remove exited containers:
docker ps --filter status=dead --filter status=exited -aq | args -r docker rm -v

# remove unused images:
docker images --no-trunc | grep '<none>' | awk '{ print $3 }' | xargs -r docker rmi
docker rmi $(docker images -aq --filter dangling=true)
docker volume ls -qf dangling=true | xargs -r docker volume rm
