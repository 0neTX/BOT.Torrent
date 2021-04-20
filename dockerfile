FROM python:3-slim
MAINTAINER "Basado en bottorrent_3.1.py" <dekkar> 
RUN pip install --upgrade pip
RUN pip install unrar cryptg telethon telethon[cryptg]

RUN useradd appuser 
WORKDIR /app
RUN mkdir /var/download
RUN mkdir /var/watch

COPY --chown=appuser:appuser bottorrent.py /app/bottorrent.py
RUN chown -R appuser /app
RUN chown -R appuser /var/download
RUN chown -R appuser /var/watch
RUN chmod 777 /app/bottorrent.py 
RUN whoami
RUN id appuser >>/app/build-data.txt
RUN date >>/app/build-data.txt
USER appuser
VOLUME ["/download", "/watch"] 
ENTRYPOINT ["python","/app/bottorrent.py"]
