# pull official base image
FROM python:3.10.1-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./requirements ./requirements
RUN pip install -r requirements.txt

# copy project
COPY . ./stunning-octo-doodle-ncap