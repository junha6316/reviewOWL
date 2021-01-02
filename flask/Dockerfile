FROM python:3.7.5
COPY . /www
WORKDIR /www
RUN apt-get update && apt-get install -y sudo
RUN pip install -r requirements.txt
CMD uwsgi uwsgi.ini