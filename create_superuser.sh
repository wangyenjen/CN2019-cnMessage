#!/bin/bash
docker exec -it $1 python manage.py createsuperuser
