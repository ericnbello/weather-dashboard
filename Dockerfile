FROM python:3.8-alpine

EXPOSE 8000

# # ENV PYTHONUNBUFFERED 1
# # ENV PYTHONDONTWRITEBYTECODE 1
# # ENV DEBIAN_FRONTEND noninteractive

RUN apk add --no-cache gcc python3-dev musl-dev postgresql-dev libpq-dev libffi-dev

ADD . /enhanced_weather_app

WORKDIR /enhanced_weather_app

COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

ARG OPENWEATHER_API_KEY
ENV OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

COPY . .