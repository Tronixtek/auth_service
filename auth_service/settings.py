# Redis cache configuration for Railway
CACHES = {
	'default': {
		'BACKEND': 'django_redis.cache.RedisCache',
		'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
		'OPTIONS': {
			'CLIENT_CLASS': 'django_redis.client.DefaultClient',
		}
	}
}
SPECTACULAR_SETTINGS = {
	"TITLE": "Auth Service API",
	"DESCRIPTION": "API documentation for the authentication service.",
	"VERSION": "1.0.0",
	"SERVE_INCLUDE_SCHEMA": False,
	"SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4.15.5",
	"REDOC_DIST": "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
}
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'changeme')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'users',
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

ROOT_URLCONF = 'auth_service.urls'

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

WSGI_APPLICATION = 'auth_service.wsgi.application'

import dj_database_url

DATABASES = {
	'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

AUTH_USER_MODEL = 'users.User'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For Railway deployment
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
	),
	'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

