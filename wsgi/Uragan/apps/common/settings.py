# coding: utf-8
"""
Django settings for Uragan project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FILES_DIRS = os.path.normpath(os.path.join(BASE_DIR, 'files'))
SERVER_FILES_DIRS = os.path.normpath(os.path.join(BASE_DIR, '..', 'static'))

ON_OPENSHIFT = False
if os.environ.get('OPENSHIFT_REPO_DIR', False):
    ON_OPENSHIFT = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('OPENSHIFT_SECRET_TOKEN', '$(@)#f)t^&!7q^s0rf=%hspn+boi81&vk%+=aye1uc@pj5+$b9')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['localhost', '127.3.161.130']
if os.environ.get('OPENSHIFT_GEAR_DNS', False):
    ALLOWED_HOSTS.append(os.environ['OPENSHIFT_GEAR_DNS'])

ADMINS = (
    ('NikitaKoshelev', 'nikita.koshelev@gmail.com'),
)
MANAGERS = ADMINS

# Application definition

DEFAULT_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'django_forms_bootstrap',
    'django_select2',
    'rosetta',
    'formtools',
)

LOCAL_APPS = (
    'apps.TLE',
    'apps.User',
    'apps.GeoObject',
)
INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'solid_i18n.middleware.SolidLocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'apps.common.urls'

WSGI_APPLICATION = 'apps.common.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if ON_OPENSHIFT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['OPENSHIFT_APP_NAME'],
            'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
            'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
            'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
            'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db', 'Uragan.sqlite3'),
            #'ENGINE': 'django.db.backends.postgresql_psycopg2',
            #'NAME': 'uragan',
            #'USER': 'admingkyfu7m',
            #'PASSWORD': 'U7TqqYT97xlW',
            #'HOST': 'uragan-nikitakoshelev.rhcloud.com',
            #'PORT': '5432',
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

LOCALE_PATHS = tuple(os.path.join(BASE_DIR, os.path.normpath(app.replace('.', '/')), 'locale') for app in LOCAL_APPS)
LOCALE_PATHS += (
     os.path.join(BASE_DIR, 'locale'),
)

# Optional. If you want to use redirects, set this to True
SOLID_I18N_USE_REDIRECTS = False

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/files/statics/'

STATIC_ROOT = os.path.join(SERVER_FILES_DIRS, 'statics')

STATICFILES_DIRS = (
    os.path.join(FILES_DIRS, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/files/media/'
MEDIA_ROOT = os.path.join(SERVER_FILES_DIRS, 'media')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Authentication--------------------------------------------------------------------------------------------------------

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'User.Profile'
#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
"""
#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20150415T224006Z.a368509643fb7c76.cf232c7e8dce21c5295d69dfcd16ee2e76aa1cf9'
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
#ROSETTA_GOOGLE_TRANSLATE = True
ROSETTA_WSGI_AUTO_RELOAD = True
#-----------------------------------------------------------------------------------------------------------------------
AUTO_RENDER_SELECT2_STATICS = False