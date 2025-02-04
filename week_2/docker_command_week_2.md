### docker run to connect to the pgadmin

1.first check if the kestra and postgres are running on the same network
2. docker run to connect to pgadmin
    docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-e PGADMIN_CONFIG_PROXY_X_HOST_COUNT=1 \
-e PGADMIN_CONFIG_PROXY_X_PREFIX_COUNT=1 \
-p 8080:80 \
--network=<network-name> \
--name pgadmin-kestra \
dpage/pgadmin4


while connecting to create new server , make sure to check docker network
**docker network inspect <network-name>**

not sure which network to run just check with 
**docker inspect <container_id> | grep "NetworkMode"**