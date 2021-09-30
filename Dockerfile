# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY requirements.txt /tmp/
COPY ./app /app
WORKDIR /app

RUN pip3 install -r /tmp/requirements.txt

CMD [ "python3", "app.py"]