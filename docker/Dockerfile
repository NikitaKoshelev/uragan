FROM python:latest

MAINTAINER NikitaKoshelev (nikita.koshelev@gmail.com)

WORKDIR /usr/src/app
ENV PYTHONPATH=/usr/src/app

RUN apt-get update && \
    apt-get install -y binutils libproj-dev gdal-bin && \
    apt-get autoclean

RUN pip install --upgrade pip setuptools wheel uwsgi

COPY requirements.txt uwsgi.ini ./
RUN pip install --no-cache-dir -Ur requirements.txt

COPY . ./

EXPOSE 8000 9191

CMD uwsgi --ini uwsgi.ini
