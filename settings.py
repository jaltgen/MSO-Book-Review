	# -*- coding: utf-8 -*-
# Django settings for mso_bookstore project.

import os.path

BASE_PATH = os.path.dirname(__file__)
SERVER_EMAIL = 'django@webserver'
DEBUG = False 
SEND_BROKEN_LINK_EMAILS = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Jannik Altgen', 'jannik.altgen@googlemail.com'),
)

MANAGERS = ADMINS

#ATABASE_ENGINE = 'sqlite3'
#DATABASE_NAME = '/srv/django/books/sqlite.db'

LDAP_URI = "ldap://10.1.0.1:389/"
LDAP_USER_BASE = "cn=users,dc=intern,dc=marienschule,dc=com"
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'books.ldap_backend.LDAPBackend')

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'mso_books'             # Or path to database file if using sqlite3.
DATABASE_USER = 'postgres'             # Not used with sqlite3.
DATABASE_PASSWORD = 'ab5-x9y'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.

DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''
UPLOAD_LOCATION = '/srv/static/upload/'
ROOT_PATH = '/buecher'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'l0f2susiqi2hp-3qo8d^e(h#s2kll3v$!r%hwz)6(s9!8&t-c)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'books.syslog_error.Syslog_Output',
)

ROOT_URLCONF = 'books.urls'
LOGIN_URL = '/buecher/'
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/srv/django/books/templates"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'books.books',
    'django.contrib.sites',
    'django.contrib.admin',
)
