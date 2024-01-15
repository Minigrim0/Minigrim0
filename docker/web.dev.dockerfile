# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y libpq-dev gcc

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry

# copy project
COPY . .

# install project dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi