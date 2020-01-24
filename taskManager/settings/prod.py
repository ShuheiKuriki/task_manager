from .common import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskmanager',
        'USER': 'django',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

SECRET_KEY = os.environ['SECRET_KEY']

import django_heroku

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.9/howto/static-files/

django_heroku.settings(locals(), staticfiles=False)
