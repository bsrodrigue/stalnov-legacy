# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# Install packages
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql \
  && apk add postgresql-dev \
  && pip install psycopg2 \
  && apk add jpeg-dev zlib-dev libjpeg \
  && pip install Pillow \
  && apk del build-deps

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOSTNAME local-stalnov.com

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./src/ ./

# Run migrations
# RUN python manage.py migrate

ENTRYPOINT ["./scripts/dev_entrypoint.sh"]
EXPOSE 8000
