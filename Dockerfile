FROM python:3.10-alpine3.17

EXPOSE 8000
RUN apk add postgresql-client build-base postgresql-dev
RUN adduser --disabled-password user
USER user

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

COPY . /app
WORKDIR /app

#RUN python manage.py migrate
#RUN python manage.py createsuperuser --noinput
ENTRYPOINT ["sh", "entrypoint.sh"]