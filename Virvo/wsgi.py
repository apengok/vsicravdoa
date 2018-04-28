"""
WSGI config for Virvo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Virvo.settings")

# application = get_wsgi_application()

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/django-work/venv/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/scada/django-work/vsicravdoa')
sys.path.append('/home/scada/django-work/vsicravdoa/Virvo')

os.environ['DJANGO_SETTINGS_MODULE'] = 'Virvo.settings'

# Activate your virtual env
activate_env=os.path.expanduser("~/django-work/venv/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()