# gunicorn config

from subprocess import call

call(["python", "manage.py", "migrate"])
call(["python", "manage.py", "loaddata",  "main/fixtures/*"])
call(["python", "manage.py", "fetch_scheludes"])

bind = "0.0.0.0:8000"


