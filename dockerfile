FROM python:3-slim
MAINTAINER "Basado en bottorrent_3.1.py" <dekkar> 
RUN pip install unrar cryptg telethon telethon[cryptg]
WORKDIR /app
COPY bottorrent.py /app/bottorrent.py
RUN chmod 777 /app/bottorrent.py 
RUN date >/app/build-date.txt
VOLUME ["/download", "/watch"] 
ENTRYPOINT ["python","/app/bottorrent.py"]
