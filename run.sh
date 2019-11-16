#!/bin/bash

python3 bmstumap_admin/manage.py dbshell << EOF
ALTER TABLE django_admin_log CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE cabinet CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE degree CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE employee CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE floor CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;

ALTER TABLE posheld CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE position CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE schedule CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
EOF

python3 bmstumap_admin/manage.py migrate

python3 bmstumap_admin/manage.py runserver

/bin/bash