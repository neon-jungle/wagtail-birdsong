from tests.app.settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'postgres',
        'NAME': 'birdsong',
        'USER': 'birdsong_dev',
        'PASSWORD': 'password',
    },
}

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail'
EMAIL_PORT = 25

INSTALLED_APPS += [
    'wagtail.contrib.styleguide'
]

import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}