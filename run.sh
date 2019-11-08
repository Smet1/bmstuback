#!/bin/bash

python3 bmstumap_admin/manage.py migrate

python3 bmstumap_admin/manage.py runserver

/bin/bash