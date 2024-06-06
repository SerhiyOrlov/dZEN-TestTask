FROM python:3.12.3-alpine
LABEL authors="sergeyorlov"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apk add --no-cache libpq
COPY ./requirements.txt /usr/src/app/tmp/requirements.txt
RUN pip install -r /usr/src/app/tmp/requirements.txt
RUN rm -r /usr/src/app/tmp/

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev
RUN rm -rf /tmp
RUN apk del .tmp-build-deps

COPY /entrypoint.sh /usr/src/app/entrypoint.sh
COPY config /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint/sh"]