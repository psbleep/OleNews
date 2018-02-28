"""
WSGI config for Ole_Mundo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv, find_dotenv


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ole_Mundo.settings")

application = get_wsgi_application()

dotenv_path = '~/Documents/Django/Ole_Mundo/Ole_Mundo/.env'
load_dotenv(find_dotenv())
