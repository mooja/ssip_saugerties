#!/bin/sh

docker-compose -f dev.yml run django python manage.py "$@"
