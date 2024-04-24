# Dockerfile

# pull the official docker image
FROM python:3.11.0-slim

# set work directory
WORKDIR /src

# set env variables
ENV APP_NAME "nginx-scale-PT"
ENV APP_VERSION 1.0
ENV REDIS_URL "redis://default:redis@app-redis-db:6379/0"

# install dependencies
COPY poetry.lock pyproject.toml ./
RUN pip3 install poetry && \
    poetry config virtualenvs.create false
RUN poetry install --no-dev

# copy project
COPY . .