# BOT.Torrent - 3.1

## Manual de uso

### Pasos previos

1. Crear nuestro BOT en Telegram y obtener su TOKEN. Obtenemos: TG_BOT_TOKEN
2. Crear nuestra App en Telegram y obtener su api_id y api_hash. 
   Entrar en https://my.telegram.org/auth y generar la api. Obtenemos: TG_API_ID y TG_API_HASH
3. Obtener user id enviando mensaje a este bot @userinfobot desde Telegram, y te devuelve tu id. Es el ID de telegram. Obtenemos: TG_USER_ID y TG_USER_NAME

## Variables de entorno necesarias

- Actualizar el fichero de variables de entorno de ejemplo 'enviroment.samples' con los valores:

```ini

TG_API_ID=8979879
TG_API_HASH=05b8825669ae9dee51934
TG_BOT_TOKEN=123412341234:218f7e864f2500b544d2f
TG_DOWNLOAD_PATH=/download
TG_USER_ID=1341341241234
TG_USER_NAME='miusuario'

```

- Renombrar el fichero con nombre '.env'

### Ejecutar mediante Docker Run

Ejecutar utilizando fichero de entorno llamado '.env'

```bash
docker run --rm -it --name bottorrent --env-file .env -v ./data/path:/download bottorrent /bin/sh
```

### Ejecutar mediante Docker Compose

Ejemplo de docker-compose.yml

```yml
version: "3.9"
services:
  bottorrent:
    container_name: bottorrent
    build:
        context: .
        dockerfile: dockerfile
    labels:
        poc.bottorrent.description: "bottorrent container"
    volumes:
        - ./data/path:/download        
        - ./data/log.txt:/app/log.txt
    env_file:
        - .env
    #Alternativamente puedes usar lo siguiente:
    #environment:
    #    - 'TG_API_ID=168'
    #    - 'TG_API_HASH=3efd8c04ad'
    #    - 'TG_BOT_TOKEN=394:S4zPd09m-p4'
    #    - 'TG_DOWNLOAD_PATH=/download'         
    #    - 'TG_USER_ID=9879874654'         
    #    - TG_USER_NAME='mi_usuario'
    restart: unless-stopped    
```

# LICENCIA

Este programa es software GRATUITO: puedes redistribuirlo y/o modificar bajo los términos de la Licencia Pública General GNU publicada por la Free Software Foundation, ya sea la versión 3 de la Licencia, o (a su elección) cualquier versión posterior.

Este programa se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA, ni RESPONSABILIDAD; sin siquiera la garantía implícita de COMERCIABILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Ver el Licencia pública general GNU para obtener más detalles <https://www.gnu.org/licenses/>.

El USUARIO de este programa, es el UNICO RESPONSABLE, de que el USO del mismo, se limita, al estricto cumplimiento, de cualquier LEY, aplicable.