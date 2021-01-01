FROM python:3.7.5
COPY . /www
WORKDIR /www
RUN apt-get update && apt-get install -y sudo
RUN pip install -r requirements.txt
RUN pip install uwsgi sqlalchemy graphene>=2.0 graphene-sqlalchemy>=2.0 google-api-python-client oauth2client
CMD uwsgi uwsgi.ini