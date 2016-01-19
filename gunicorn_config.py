# gunicorn config

from subprocess import call

call(["python", "manage.py", "migrate"])
call(["python", "manage.py", "loaddata",  "main/fixtures/*"])
call(["python", "manage.py", "fetch_scheludes"])

bind = ["127.0.0.1:8000", "0.0.0.0:8080"]


