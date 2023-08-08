FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN mkdir /app
WORKDIR /usr/app

COPY requirements.txt .
RUN apt-get update \
    && apt-get install -yyq ncat
RUN pip install -r requirements.txt

COPY . .


#COPY /docker/entrypoint.sh .


EXPOSE 8000
