"""
Django settings for logicPuzzle project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import ssl
import sys

<<<<<<< HEAD
import sys
import os
from pathlib import Path
from django.conf import settings
from dotenv import load_dotenv
import os.path

load_dotenv()
GOOGLE_API_KEY = os.getenv('AIzaSyDdE-VBMf-WDKNFHSWpbRgBlcAZwe9TaCI')

=======
import certifi
import environ

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
>>>>>>> f3f07d4aaf9b8d04c7fc7f30a7bcb65d851258d2



import db_settings
from django.conf import settings
from dotenv import load_dotenv
import db_settings

# Load environment variables
load_dotenv()

# Google API Key (make sure to load it from .env instead)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SSL 인증서와 키 파일 경로 지정
SSL_CERT_FILE = os.path.join(BASE_DIR, 'ssl', 'server.cert')
SSL_KEY_FILE = os.path.join(BASE_DIR, 'ssl', 'server.key')

# SSL 컨텍스트 생성
#EMAIL_SSL_CONTEXT = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#EMAIL_SSL_CONTEXT.load_cert_chain(certfile=SSL_CERT_FILE, keyfile=SSL_KEY_FILE)
#EMAIL_SSL_CONTEXT.options |= ssl.OP_NO_SSLv2
#EMAIL_SSL_CONTEXT.options |= ssl.OP_NO_SSLv3

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
<<<<<<< HEAD
SECRET_KEY = os.getenv("SECRET_KEY")
=======
SECRET_KEY = env('SECRET_KEY')
>>>>>>> f3f07d4aaf9b8d04c7fc7f30a7bcb65d851258d2

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

<<<<<<< HEAD

ALLOWED_HOSTS = ["*"]
=======
ALLOWED_HOSTS = ['*']
>>>>>>> f3f07d4aaf9b8d04c7fc7f30a7bcb65d851258d2


# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'production',
    'food_waste',
    'notice',
    'user',
<<<<<<< HEAD
=======
    'profile',
>>>>>>> f3f07d4aaf9b8d04c7fc7f30a7bcb65d851258d2
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'logicPuzzle.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'logicPuzzle.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '3306',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = False  # TLS를 사용할 경우 True로 설정하지 않음
#EMAIL_SSL_CERTFILE = SSL_CERT_FILE
#EMAIL_SSL_KEYFILE = SSL_KEY_FILE
#EMAIL_SSL_CONTEXT = EMAIL_SSL_CONTEXT

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False

APPEND_SLASH = False

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'file_name.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'app_name': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


CACHES = {
    "default": {
        "BACKEND": 'django_redis.cache.RedisCache',
        "LOCATION": 'redis://redis_service:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

#celery
CELERY_BROKER_URL = 'localhost:6379'
CELERY_RESULT_BACKEND = 'localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

SWAGGER_SETTINGS = {
   'USE_SESSION_AUTH': False
}

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

