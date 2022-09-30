FROM python:3-slim AS basebottorrent

RUN set -e; \
    pip install --upgrade pip; \
    pip install unrar cryptg telethon telethon[cryptg]

FROM basebottorrent

ARG UID=99
ARG GID=1000
ENV TG_DOWNLOAD_PATH=/var/download
ENV TG_WATCH_PATH=/var/watch

COPY --chown=bottorrent:bottorrent bottorrent.py /app/bottorrent.py

RUN set -e; \
    mkdir ${TG_WATCH_PATH}; \
    mkdir ${TG_DOWNLOAD_PATH}; \
    addgroup --gid $GID bottorrent; \
    useradd -m -u $UID -g $GID -d /app bottorrent; \
    chown -R bottorrent:bottorrent /app ${TG_DOWNLOAD_PATH} ${TG_WATCH_PATH}; \
    chmod 555 /app/bottorrent.py 

WORKDIR /app

USER bottorrent

VOLUME ${TG_DOWNLOAD_PATH} ${TG_WATCH_PATH}

ENTRYPOINT ["python","/app/bottorrent.py"]