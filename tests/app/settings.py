import os

INSTALLED_APPS = [
    'birdsong',
    'tests.app',

    'mjml',
    'taggit',
    'modelcluster',

    'wagtail.core',
    'wagtail.admin',
    'wagtail.users',
    'wagtail.sites',
    'wagtail.snippets',
    'wagtail.images',
    'wagtail.documents',
    'wagtail.contrib.modeladmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

SECRET_KEY = 'not a secret'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'postgres',
        'NAME': 'birdsong',
        'USER': 'birdsong_dev',
        'PASSWORD': 'password',
        'TEST': {'NAME': 'test'},
    }
}

if 'POSTGRES_DB' in os.environ:
    DATABASES['default'].update({
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'postgres',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
    })

ROOT_URLCONF = 'tests.app.urls'

WAGTAIL_SITE_NAME = 'Birdsong'

DEBUG = True

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

MJML_BACKEND_MODE = 'tcpserver'
MJML_TCPSERVERS = [
    ('mjml', 28101),  # host and port
]

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
MEDIA_URL = '/media/'

WAGTAILADMIN_BASE_URL = "localhost:8080"
