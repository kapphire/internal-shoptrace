"""
Django settings for interShoptrace project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from kombu import Queue
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zhebj7guvi!wcomk$39&3-hgsu$6xxl49^+2j-91ztf5od&fsq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # My APP
    'common',
    'users',
    'links',
    # External packages
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'notifications',
    'django_tables2',
    'django_filters',
    'bootstrap4',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'interShoptrace.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'interShoptrace.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'internal_shoptrace',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
# os.environ['DATABASE_URL'] = 'postgres://mmxccvygngqncs:c576723b7f4ce7ac03f4c9dfb9450e87459bd0a14a12768bf46a880a2aceea19@ec2-54-197-232-203.compute-1.amazonaws.com:5432/d2flo5485f32gb'

# if 'DATABASE_URL' in os.environ:
#     db_from_env = dj_database_url.config(conn_max_age=500)
#     DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

AUTH_USER_MODEL = 'users.ShoptraceUser'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Allauth Configurations
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/link/'

# FIREBASE DATABASE CONFIGURATION
FIREBASE_CONFIG = {
    "apiKey" : 'AIzaSyCl40ugLIaQfgxRFw_7_DKaZ-_aEAQiiWU',
    "authDomain" : 'shoptrace-98e1b.firebaseapp.com',
    "databaseURL" : 'https://shoptrace-98e1b.firebaseio.com',
    "storageBucket" : 'shoptrace-98e1b.appspot.com'
}

# DAYS FROM NOW
PERIOD = 7

# Django Tables 2
DJANGO_TABLES2_TEMPLATE = os.path.join(BASE_DIR, 'templates/django_tables2/table.html')
DJANGO_TABLES2_PAGINATE_BY = 20
DJANGO_TABLES2_TABLE_STYLE = {
    'class': 'table table-striped table-bordered',
}

# CRISPY FORM SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Determines if the library will use database transactions on data import, just to be on the safe side.
IMPORT_EXPORT_USE_TRANSACTION = True

# Set this to make GDAL work in Heroku
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')

# CELERY CONFIGURATION
CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL') or os.environ.get("CELERY_BROKER_URL", 'amqp://localhost')
CELERY_ACCPET_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default'),
    Queue('inventory'),
)
CELERY_CREATE_MISSING_QUEUES = True
readbeat_redis_url = os.getenv('REDBEAT_REDIS_URL', CELERY_RESULT_BACKEND)
