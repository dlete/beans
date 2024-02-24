"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()

# added by dlete to publish in Heroku. Following instructions in:
# https://github.com/DjangoGirls/tutorial-extensions/blob/master/heroku/README.md
from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)
