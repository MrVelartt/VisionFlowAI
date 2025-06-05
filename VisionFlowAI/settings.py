# VisionFlowAI/settings.py

from pathlib import Path
import os
from dotenv import load_dotenv
import logging

# 1. BASE_DIR y carga de .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# 2. Claves y configuración de AWS S3
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')  # p.ej. 'us-east-2'

# Si tu bucket no usa ACLs, deja None; de lo contrario, podrías poner 'public-read'
AWS_DEFAULT_ACL = None

# Para que las URLs que genere no incluyan firma (si tu bucket es público)
AWS_QUERYSTRING_AUTH = False

# (Opcional) Parámetros por defecto para cada objeto en S3
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}


STORAGES = {
    # Backend “default” para archivos ‘media’ (FileField, ImageField, etc.)
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "default_acl": AWS_DEFAULT_ACL,
            "querystring_auth": AWS_QUERYSTRING_AUTH,
            "location": "",
            "object_parameters": AWS_S3_OBJECT_PARAMETERS,
        },
    },
    # Backend para archivos estáticos; aquí usamos el almacenamiento local de Django
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# 4. Ajustes generales de Django
SECRET_KEY = 'django-insecure-bvll*cixf(_5d(!6j%&g_b(ywptu6bwza%8^kgsi@b6!2)w-9m'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_yasg',

    'storages',       # debe ir antes de VisionAI
    'VisionAI',
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

ROOT_URLCONF = 'VisionFlowAI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # aquí tus carpetas de plantillas (si las hubiera)
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

WSGI_APPLICATION = 'VisionFlowAI.wsgi.application'


# 5. Base de datos PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbfacturas',
        'USER': 'postgres',
        'PASSWORD': 'Voluntad1',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# 6. Validación de contraseñas
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


# 7. Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# 8. Archivos estáticos
STATIC_URL = '/static/'
# Si habilitas STORAGES["staticfiles"], Django usará ese backend al hacer collectstatic.

# 9. Configuración de REST Framework (mínima)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}


# 10. Logging de boto3/botocore (opcional, para depuración)
logging.basicConfig(level=logging.INFO)
logging.getLogger('boto3').setLevel(logging.DEBUG)
logging.getLogger('botocore').setLevel(logging.DEBUG)


# 11. Configuración final
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
