FROM python:3.8.17-alpine

RUN apk --update --upgrade add py3-pip py3-pillow py3-cffi py3-brotli gcc musl-dev python3-dev pango libffi-dev jpeg-dev

ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    DJANGO_SETTINGS_MODULE=rms.settings

RUN pip3 install poetry

WORKDIR /app
COPY . /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev
RUN sh init.sh