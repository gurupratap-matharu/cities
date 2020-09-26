# Pull base image
FROM python:3.7

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work dir
WORKDIR /code

# install requirements
COPY requirements.txt /code/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# install gdal
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

# copy project
COPY . /code/