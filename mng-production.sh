#!/bin/sh

docker-compose -f docker-compose.yml run django python manage.py "$@"
