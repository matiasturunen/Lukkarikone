
import os

dev = os.environ.get("DEV", False)

if (dev == "True"):
    # development settings
    from .dev import * 
    print ("Using development settings!!")
else:
    # production settings
    from .prod import * 
    print ("Using production settings!!")

##### DJANGO SECRETS
SECRET_KEY = os.environ.get("SECRET_KEY", "use_env_variable_as_secret_key")
