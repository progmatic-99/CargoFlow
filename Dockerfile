# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE=rms.settings
ENV DEBUG=True

# Install system dependencies and poetry
RUN apt-get update && apt-get install -y \
    apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 -y \
    libpq-dev && \
    curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory in the container
WORKDIR /app

COPY . /app/

# Install dependencies using poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi
