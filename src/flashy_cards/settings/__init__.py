import os
from .base import *

APP_ENV = os.environ["APP_ENV"]

if(APP_ENV == "production"):
    from .production import *
else:
    from .development import *