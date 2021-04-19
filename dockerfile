FROM python:3-slim
MAINTAINER "Basado en bottorrent_3.1.py" <dekkar> 
RUN pip install unrar cryptg telethon telethon[cryptg]
WORKDIR /app
COPY bottorrent.py /app/bottorrent.py
RUN chmod 777 /app/bottorrent.py 
RUN chown -R 99:100 /app
RUN date >/app/build-date.txt
USER 99:100 
ENTRYPOINT ["python","/app/bottorrent.py"]
