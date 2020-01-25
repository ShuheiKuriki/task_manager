from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9bv70a@#p8+0%g!))k7!%o0t%ier9u8_#yj8vi)qwo9nk7ca0h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskmanager',
        'USER': 'django',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5431'
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "develop",
        },
    },
    "formatters": {
        "develop": {
            "format": "\t".join(
                [
                    "[%(levelname)s]",
                    "%(asctime)s",
                    "%(pathname)s",
                    "%(lineno)d",
                    "%(message)s",
                ]
            )
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
