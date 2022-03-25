import os

import typing as tp

from pathlib import Path

from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='123')  # type: ignore

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', default=True)  # type: ignore

# MANAGEMENT HOSTS AND CORS
ALLOWED_HOSTS: tp.List[str] = os.environ.get('ALLOWED_HOSTS', default='').split(',')  # type: ignore
CSRF_TRUSTED_ORIGINS: tp.List[str] = os.environ.get('CSRF_TRUSTED_ORIGINS', default='').split(',')  # type: ignore
# CORS_ALLOWED_ORIGINS: tp.List[str] = os.environ.get('CORS_ALLOWED_ORIGINS', default='').split(',')  # type: ignore
# TODO update this(can be on stage, not prod)
CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',

    'rest_framework',

    'drf_yasg',

    'api.authenticate',
    'api.master',
    'api.order',
    'api.telegram_bot',
    'api.account',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ommy_polland.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ommy_polland.wsgi.application'

# Database
SQL_ENGINE = os.environ.get("SQL_ENGINE", default="django.db.backends.sqlite3")  # type: ignore
SQL_DATABASE = os.environ.get("SQL_DATABASE", default=os.path.join(BASE_DIR, "db.sqlite3"))  # type: ignore
SQL_USER = os.environ.get("SQL_USER", default="user")  # type: ignore
SQL_PASSWORD = os.environ.get("SQL_PASSWORD", default="password")  # type: ignore
SQL_HOST = os.environ.get("SQL_HOST", default="localhost")  # type: ignore
SQL_PORT = os.environ.get("SQL_PORT", default="5432")  # type: ignore

DATABASES = {
    "default": {
        "ENGINE": SQL_ENGINE,
        "NAME": SQL_DATABASE,
        "USER": SQL_USER,
        "PASSWORD": SQL_PASSWORD,
        "HOST": SQL_HOST,
        "PORT": SQL_PORT,
    }
}

# Password validation

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

# REST FRAMEWORK settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PERMISSIONS_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'PAGE_SIZE': 20,
}

# SIMPLE JWT SETTINGS
ACCESS_TOKEN_LIFETIME = int(os.environ.get('ACCESS_TOKEN_LIFETIME', 20))
REFRESH_TOKEN_LIFETIME = int(os.environ.get('REFRESH_TOKEN_LIFETIME', 60))
ALGORITHM = os.environ.get('ALGORITHM')
AUTH_HEADER_TYPES = os.environ.get('AUTH_HEADER_TYPES')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=ACCESS_TOKEN_LIFETIME),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=REFRESH_TOKEN_LIFETIME),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': ALGORITHM,
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': (AUTH_HEADER_TYPES,),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# CREDENTIALS FOR DEFAULT SUPERUSER
DEFAULT_SUPER_USER_USERNAME = os.environ.get('DEFAULT_SUPER_USER_USERNAME')  # type: ignore
DEFAULT_SUPER_USER_PASSWORD = os.environ.get('DEFAULT_SUPER_USER_PASSWORD')  # type: ignore
DEFAULT_SUPER_USER_EMAIL = os.environ.get('DEFAULT_SUPER_USER_EMAIL')  # type: ignore

# SET CUSTOM USER MODEL
AUTH_USER_MODEL = 'account.User'

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TIME_ZONE', default='Europe/Moscow')  # type: ignore

CELERY_TIME_ZONE = os.environ.get('TIME_ZONE', default='Europe/Moscow')  # type: ignore

USE_I18N = True

USE_L10N = True

USE_TZ = True

# REDIS
REDIS_HOST = os.environ.get('REDIS_HOST')  # type: ignore
REDIS_PORT = os.environ.get('REDIS_PORT')  # type: ignore

# CELERY
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'  # type: ignore
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'  # type: ignore

# TELEGRAM SETTINGS
BOT_TOKEN = os.environ.get('BOT_TOKEN')  # type: ignore
ORDER_CHAT_ID = os.environ.get('ORDER_CHAT_ID')  # type: ignore
STAGE_BOT_TOKEN = os.environ.get('STAGE_BOT_TOKEN')  # type: ignore
STAGE_ORDER_CHAT_ID = os.environ.get('STAGE_ORDER_CHAT_ID')  # type: ignore
ADMINS_CHAT_IDS = os.environ.get('ADMINS', default='').split(',')  # type: ignore

# AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')  # type: ignore
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')  # type: ignore
ORDER_BUCKET = os.environ.get('ORDER_BUCKET')  # type: ignore
BUCKET_REGION = os.environ.get('BUCKET_REGION')  # type: ignore

# TWILIO
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')  # type: ignore
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')  # type: ignore
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')  # type: ignore

# STATIC FILES
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# MEDIA FILES
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
