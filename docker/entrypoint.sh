#!/bin/sh


echo "Waiting for redis..."

while ! nc -z $REDIS_HOST 6379; do
  sleep 1
done
sleep 8
echo "Redis started"

# python manage.py flush --no-input

