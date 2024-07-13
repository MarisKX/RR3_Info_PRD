FROM python:3.11-alpine3.18
LABEL maintainer="mariskx"
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-client build-base postgresql-dev

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

ENV PATH="/py/bin:$PATH"

COPY ./django_backend /c
WORKDIR /django_backend
