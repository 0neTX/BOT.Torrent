# BOT.Torrent - Como ...

## Compilar la imagen en local

´´´bash
docker-compose -f .\docker-compose.build.yml up --build  --abort-on-container-exit --remove-orphans  --force-recreate
´´´

## Ejecutar una consola en un nuevo contenedor

´´´bash
docker run --rm -it --name bottorrent --env-file .env -v $pwd/data/path:/download  -v $pwd/data/watch:/watch --entrypoint /bin/bash bottorrent:3.2
´´´

## Ejecutar una consola en un contenedor existente

´´´bash
docker exec -it  bottorrent /bin/sh
´´´
