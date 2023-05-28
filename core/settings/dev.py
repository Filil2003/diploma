""" Settings for local development. """
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

YOOKASSA_SHOP_ID = getenv('YOOKASSA_SHOP_ID')
YOOKASSA_SECRET_KEY = getenv('YOOKASSA_SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = getenv('DJANGO_SECRET_KEY')

DEBUG = True

if getenv('DJANGO_ALLOWED_HOSTS'):
    ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS').split(',')
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

if getenv('DJANGO_CSRF_TRUSTED_ORIGINS'):
    ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS').split(',')
else:
    CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

INSTALLED_APPS = (
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'formtools',
    'autoslug',
    'utils',
    'accounts',
    'cleaning',
    'orders',
    'payment'
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

ROOT_URLCONF = 'core.urls'

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (BASE_DIR / 'templates',),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cleaning.context_processors.services'
            )
        }
    },
)

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTH_PASSWORD_VALIDATORS = (
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 3,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'test@gmail.com'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

USE_THOUSAND_SEPARATOR = True

AUTH_USER_MODEL = 'accounts.Account'
LOGIN_REDIRECT_URL = 'cleaning:home'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
