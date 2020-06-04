from tests.app.settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'local.sqlite3',
    },
}

ALLOWED_HOSTS = ['*']
