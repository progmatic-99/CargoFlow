FROM python:3.8.17-alpine
ENV PYTHONUNBUFFERED=1
RUN apk --update --upgrade add py3-pip py3-pillow py3-cffi py3-brotli gcc musl-dev python3-dev pango libffi-dev jpeg-dev

ENV DJANGO_SETTINGS_MODULE=rms.settings

WORKDIR /app
COPY . /app/
RUN pip3 install -r requirements.txt
RUN sh init.sh
