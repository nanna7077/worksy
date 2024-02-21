# syntax=docker/dockerfile:1

FROM python:3.12-slim-buster

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY . ./

RUN pip3 install --no-cache-dir -r requirements.txt

CMD exec python3 pywsgi.py