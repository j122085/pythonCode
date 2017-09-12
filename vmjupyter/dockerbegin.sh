#!/bin/bash

docker run -itd --name redisco -p 8001:6379 -v /home/j122085/redisdata:/data j122085/redis
docker run -itd --name jupyterco  -p 8000:8888 --link redisco:redis -v /home/j122085/jupyterCode:/home/jovyan/facets j122085/jupyter start-notebook.sh --NotebookApp.password='sha1:99e1e69d9c96:a8b7e4295b0964af5a3a1830c53da69e387b4834'
docker run --name mariaco -d -p 8003:3306 -v /home/j122085/mariadb:/var/lib/mysql --link jupyterco:jupyter -e MYSQL_ROOT_PASSWORD=850605 j122085/maria


