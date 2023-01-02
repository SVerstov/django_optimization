FROM python:3.10-alpine3.17

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

EXPOSE 8000


RUN adduser --disabled-password user

USER user

COPY . /app
WORKDIR /app
