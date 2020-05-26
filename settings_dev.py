from tests.app.settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'local.sqlite3',
    },
}

ALLOWED_HOSTS = ['*']

MJML_BACKEND_MODE = 'tcpserver'
MJML_TCPSERVERS = [
    ('mjml', 28101),  # host and port
]