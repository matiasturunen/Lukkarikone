# gunicorn config

from django.core import management

bind = ["127.0.0.1:8000", "0.0.0.0:8080"]


def pre_fork(server, worker):
    #management.call_command("migrate")
    #management.call_command("loaddata", "main/fixtures/*")
    #management.call_command("fetch_scheludes")
    
    pass
