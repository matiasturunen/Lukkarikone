# Lukkarikone

Tool for searching courses available at LUT

Rename settings/"\_\_init\_\_"EXAPLE.py to \_\_init\_\_.py and make it to match your preferred settings

Commands to start dev/prod easily
Set up database
``` python manage.py migrate ```
Add fixtures
``` ./add-fixtures ```
Load schelude data. (repeat until success = True)
``` python manage.py fetch_scheludes ```
Run server
``` ./run-dev-server ```