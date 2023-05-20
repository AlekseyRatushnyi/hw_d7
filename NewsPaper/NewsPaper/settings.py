import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3+!+0$lw9lb6n&*v6lo%v50ud1h7qo2$r9c7(23oi8^25^ap+p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'modeltranslation', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'sign',
    'protect',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'news.apps.NewsConfig',
    'django_apscheduler',
    'basic',

]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'basic.middlewares.TimezoneMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'NewsPaper/news/templates')],
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

LANGUAGES =[
    ('en-us', 'English'),
    ('ru', 'Русский')
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SATICFILES_DIRS = [BASE_DIR / 'static']

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/posts'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_FORMS = {'signup': 'sign.models.BasicSignupForm'}

SITE_URL = 'http://127.0.0.1:8000/'

EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = 'AARatushnyi@yandex.ru'
EMAIL_HOST_PASSWORD = '04122012Matt#$'  # пароль от почты
EMAIL_USE_SSL = True  # Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ADMINS = [
    ('RatushnyiAA', 'RatushnyiAA@bk.ru'), ('RatushnyiAA1982', 'RatushnyiAA1982@gmail.com'),
    # список всех админов в формате ('имя', 'их почта')
]

MANAGERS = [
    ('RatushnyiAA1982', 'RatushnyiAA1982@gmail.com'), ('RatushnyiAA', 'RatushnyiAA@bk.ru'),
    # список всех менеджеров в формате ('имя', 'их почта')
]

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        'TIMEOUT': 30,
    }
}
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'style': '{',
    'formatters': {
        'fdebug': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        },
        'fwarning': {
            'format': '%(asctime)s - %(levelname)s - %(message)s -%(pathname)s',
        },
        'ferror': {
            'format': '%(asctime)s - %(levelname)s - %(message)s -%(pathname)s-%(exc_info)s'
        },
        'gfile': {
            'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
        },
        'erfile': {
            'format': '%(asctime)s - %(levelname)s - %(message)s -%(pathname)s-%(exc_info)s'
        },
        'srfile': {
            'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
        },
        'mailfile': {
            'format': '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s'
        },

    },
    'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            }
         },
    'handlers': {
        'fdebug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'fdebug',
            'filters': ['require_debug_true']
        },
        'fwarning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'fwarning',
            'filters': ['require_debug_true']
        },
        'ferror': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'ferror',
            'filters': ['require_debug_true']
        },
        'gfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'gfile',
            'filename': 'general.log',
            'filters': ['require_debug_false']
        },
        'erfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'erfile',
            'filename': 'errors.log',
        },
        'srfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'srfile',
            'filename': 'security.log',
        },
        'mailfile': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mailfile'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['fdebug', 'fwarning', 'ferror', 'gfile'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['erfile', 'mailfile'],
            'propagate': True,
        },
        'django.server': {
            'handlers': ['erfile', 'mailfile'],
            'propagate': True,
        },
        'django.template': {
            'handlers': ['erfile'],
            'propagate': True,
        },
        'django.db_backends': {
            'handlers': ['erfile'],
            'propagate': True,
        },
        'django.security': {
            'handlers': ['srfile'],
            'propagate': True,
        },
    }
}