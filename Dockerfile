FROM python:3.7-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./req.txt req.txt
RUN pip install -r req.txt
RUN pip install gunicorn

RUN apt-get update && apt-get install netcat -y

COPY ./tga /app/tga
COPY ./manage.py /app/manage.py
COPY ./ugc /app/ugc
RUN mkdir /app/static
RUN python manage.py collectstatic --no-input --clear