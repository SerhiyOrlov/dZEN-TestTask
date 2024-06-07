FROM python:3.12.3-alpine
LABEL authors="sergeyorlov"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt
# Установка зависимостей
RUN apk add --update --no-cache \
    postgresql-client \
    build-base \
    postgresql-dev \
    musl-dev && \
    pip install --no-cache-dir -r requirements.txt


COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
