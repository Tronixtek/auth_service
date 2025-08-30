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

SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
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

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ.get('POSTGRES_DB', 'auth_db'),
		'USER': os.environ.get('POSTGRES_USER', 'auth_user'),
		'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'auth_pass'),
		'HOST': os.environ.get('DB_HOST', 'db'),
		'PORT': os.environ.get('DB_PORT', '5432'),
	}
}

AUTH_USER_MODEL = 'users.User'

STATIC_URL = '/static/'

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
	),
	'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

