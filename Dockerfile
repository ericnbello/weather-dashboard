FROM python:3.8-alpine

EXPOSE 8000

# # ENV PYTHONUNBUFFERED 1
# # ENV PYTHONDONTWRITEBYTECODE 1
# # ENV DEBIAN_FRONTEND noninteractive
ARG openweather_api_key

RUN apk add --no-cache gcc python3-dev musl-dev postgresql-dev libpq-dev libffi-dev

ADD . /enhanced_weather_app

WORKDIR /enhanced_weather_app

COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
#RUN pip3 install httpx
#RUN pip install --no-cache-dir --upgrade pip
# # RUN pip install gunicorn==20.1.0
# RUN python3 -m pip install setuptools
# RUN pip install --upgrade pip
# RUN pip3 install httpx
#RUN pip install -r requirements.txt 

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

COPY . .
# # FROM python:3.10-slim-buster

# # # Open http port
# # EXPOSE 8000

# # ENV PYTHONUNBUFFERED 1
# # ENV PYTHONDONTWRITEBYTECODE 1
# # ENV DEBIAN_FRONTEND noninteractive

# # # Install pip and gunicorn web server
# # RUN pip install --no-cache-dir --upgrade pip
# # # RUN pip install gunicorn==20.1.0
# # RUN python3.10 -m pip install setuptools

# # # Moving application files
# # WORKDIR /app
# # COPY . /app

# # # Install requirements.txt
# # COPY requirements.txt .
# # RUN pip install -r requirements.txt


# FROM ubuntu:20.04
# ADD . /app
# WORKDIR /app
# # ENV PYTHONPATH=/enhanced_weather_app
# RUN apt-get update -y
# RUN apt-get install software-properties-common
# RUN apt-get update
# RUN add-apt-repository ppa:deadsnakes/ppa
# # Install py39 from deadsnakes repository
# RUN apt-get install python3.8
# # Install pip from standard ubuntu packages
# RUN apt-get install python3-pip

# # RUN apt-get update -y
# # RUN sudo apt-get install python3-distutils-extra
# # RUN apt-get install python3-apt
# # RUN apt-get install software-properties-common -y
# # RUN add-apt-repository ppa:deadsnakes/ppa
# # RUN apt-get install python3.8 -y
# # RUN apt-get install python3-pip -y
# # RUN python3.8 -m pip install --upgrade pip
# RUN python3.8 -m pip install --upgrade setuptools
# RUN apt-get install sudo ufw build-essential libpq-dev libmysqlclient-dev python3.8-dev default-libmysqlclient-dev libpython3.8-dev -y
# RUN python3.8 -m pip install -r requirements.txt
# # RUN python3.9 -m pip install psycopg2-binary
# # RUN python3.9 -m pip install httpx
# RUN sudo ufw allow 8000
# EXPOSE 8000

# # # pull official base image
# # FROM python:3.9.0-slim-buster

# # # set work directory
# # WORKDIR /usr/src/enhanced_weather_app

# # # set environment variables
# # ENV PYTHONDONTWRITEBYTECODE 1
# # ENV PYTHONUNBUFFERED 1

# # # install dependencies
# # RUN pip install --upgrade pip
# # COPY ./requirements.txt .
# # RUN pip install -r requirements.txt

# # # copy project
# # COPY . .



# # The first instruction is what image we want to base our container on
# # We Use an official Python runtime as a parent image
# # FROM python:3.8

# # # Allows docker to cache installed dependencies between builds
# # COPY requirements.txt requirements.txt
# # RUN pip install --upgrade pip
# # RUN pip install --no-cache-dir -r requirements.txt

# # # Mounts the application code to the image
# # COPY . app
# # WORKDIR /app

# # EXPOSE 8000

# # # runs the production server
# # ENTRYPOINT ["python", "manage.py"]
# # CMD ["runserver", "0.0.0.0:8000"]