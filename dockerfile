FROM python:3-slim AS baseBOTTorrent

RUN set -e; \
    pip install --upgrade pip; \
    pip install unrar cryptg telethon telethon[cryptg]

FROM baseBOTTorrent

ARG UID=99
ARG GID=100
ENV TG_DOWNLOAD_PATH=/download

COPY --chown=bottorrent:bottorrent bottorrent.py /app/bottorrent.py

RUN set -e; \
    mkdir /{watch,${TG_DOWNLOAD_PATH}}; \
    addgroup --gid $GID bottorrent; \
    useradd -m -u $UID -g $GID -d /app bottorrent; \
    chown -R bottorrent:bottorrent /app ${TG_DOWNLOAD_PATH} /watch; \
    chmod 555 /app/bottorrent.py 

WORKDIR /app

USER bottorrent

VOLUME [${TG_DOWNLOAD_PATH}, "/watch"]

ENTRYPOINT ["python","/app/bottorrent.py"]
