"""
Django settings for dashboard project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import json

from debug_toolbar import settings as dt_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APPLICATION_DIR = os.path.dirname(globals()['__file__'])

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)

if os.getenv("ENV_JSON"):
    # optionally load settings from an environment variable
    ENV = json.loads(os.getenv("ENV_JSON"))
else:
    # else try loading settings from the json config file
    try:
        with open(os.getenv("ENV_FILE", "/secrets/env.json")) as f:
            ENV = json.load(f)
    except FileNotFoundError as fnfe:
        print("Default config file or one defined in environment variable ENV_FILE not found. This is normal for the build, should define for operation")
        # Set ENV so collectstatic will still run in the build
        ENV = os.environ

LOGOUT_URL = '/accounts/logout'
LOGIN_URL = '/accounts/login'
HELP_URL = ENV.get("HELP_URL", "https://sites.google.com/umich.edu/my-learning-analytics-help/home")

# Google Analytics ID
GA_ID = ENV.get('GA_ID', '')

# Resource values from env
RESOURCE_VALUES = ENV.get("RESOURCE_VALUES", {"files": {"types": ["canvas"], "icon": "fas fa-file fa-lg"}})

# Convience map to be able to get from types
RESOURCE_VALUES_MAP = {
    resource_type : resource_value
    for resource_value in RESOURCE_VALUES
    for resource_type in RESOURCE_VALUES.get(resource_value).get('types')
}

# This is required by flatpages flow. For Example Copyright information in the footer populated from flatpages
SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV.get('DJANGO_DEBUG', True)

ALLOWED_HOSTS = ENV.get("ALLOWED_HOSTS", ["127.0.0.1", "localhost"])

WATCHMAN_TOKEN = ENV.get('DJANGO_WATCHMAN_TOKEN', None)

WATCHMAN_TOKEN_NAME = ENV.get('DJANGO_WATCHMAN_TOKEN_NAME', 'token')

# Only report on the default database
WATCHMAN_DATABASES = ('default',)

# courses_enabled api
COURSES_ENABLED = ENV.get('COURSES_ENABLED', False)

# Defaults for PTVSD
PTVSD_ENABLE = ENV.get("PTVSD_ENABLE", False)
PTVSD_REMOTE_ADDRESS = ENV.get("PTVSD_REMOTE_ADDRESS", "0.0.0.0")
PTVSD_REMOTE_PORT = ENV.get("PTVSD_REMOTE_PORT", 3000)
PTVSD_WAIT_FOR_ATTACH = ENV.get("PTVSD_WAIT_FOR_ATTACH", False)

# Application definition

INSTALLED_APPS = [
    'dashboard',
    'django_ptvsd',
    'django_su',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'graphene_django',
    'django_cron',
    'watchman',
    'macros',
    'debug_toolbar',
    'pinax.eventlog',
    'webpack_loader',
    'rules.apps.AutodiscoverRulesConfig',
]

# The order of this is important. It says DebugToolbar should be on top but
# The tips has it on the bottom
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

CRON_CLASSES = [
    "dashboard.cron.DashboardCronJob",
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APPLICATION_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': ENV.get('DJANGO_TEMPLATE_DEBUG', DEBUG),
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django_su.context_processors.is_su',
                'django_settings_export.settings_export',
                'dashboard.context_processors.get_git_version_info',
                'dashboard.context_processors.get_myla_globals',
                'dashboard.context_processors.last_updated'
            ],
        },
    },
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

GRAPHENE = {
    'SCHEMA': 'dashboard.graphql.schema.schema'
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

NPM_FILE_PATTERNS = {
    'bootstrap': ['dist/css/*'],
    'jquery': ['dist/jquery.min.js'],
    '@fortawesome': ['fontawesome-free/*']
}

ROOT_URLCONF = 'dashboard.urls'

WSGI_APPLICATION = 'dashboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': ENV.get('MYSQL_ENGINE', 'django.db.backends.mysql'),
        'NAME': ENV.get('MYSQL_DATABASE', 'student_dashboard'),  # your mysql database name
        'USER': ENV.get('MYSQL_USER', 'student_dashboard_user'), # your mysql user for the database
        'PASSWORD': ENV.get('MYSQL_PASSWORD', 'student_dashboard_password'), # password for user
        'HOST': ENV.get('MYSQL_HOST', 'localhost'),
        'PORT': ENV.get('MYSQL_PORT', 3306),
    },
    'DATA_WAREHOUSE': {
        'ENGINE': ENV.get('DATA_WAREHOUSE_ENGINE', 'django.db.backends.postgresql'),
        'NAME': ENV.get('DATA_WAREHOUSE_DATABASE', ''),
        'USER': ENV.get('DATA_WAREHOUSE_USER', ''),
        'PASSWORD': ENV.get('DATA_WAREHOUSE_PASSWORD', ''),
        'HOST': ENV.get('DATA_WAREHOUSE_HOST', ''),
        'PORT': ENV.get('DATA_WAREHOUSE_PORT', 5432),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = ENV.get("TIME_ZONE", ENV.get("TZ", "America/Detroit"))

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

NPM_ROOT_PATH = BASE_DIR

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'npm.finders.NpmFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# The hex value to be used in the front end for the "primary" color of the palette and theme.
PRIMARY_UI_COLOR = ENV.get("PRIMARY_UI_COLOR", None)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # Gunicorns logging format https://github.com/benoitc/gunicorn/blob/19.x/gunicorn/glogging.py
    'formatters': {
        "generic": {
            "format": "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': ENV.get('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'rules': {
            'handlers': ['console'],
            'propagate': False,
            'level': ENV.get('RULES_LOG_LEVEL', 'INFO'),
        },
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
        },

    },
    'root': {
        'level': ENV.get('ROOT_LOG_LEVEL', 'INFO'),
        'handlers': ['console']
    },
}


# IMPORT LOCAL ENV
# =====================
try:
    from settings_local import *
except ImportError:
    pass

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django_su.backends.SuBackend',
)

#Shib

# Give an opportunity to disable SAML
if ENV.get('STUDENT_DASHBOARD_SAML', True):
    import saml2

    SAML2_URL_PATH = '/accounts/'
    # modify to use port request comes
    SAML2_URL_BASE = ENV.get('DJANGO_SAML2_URL_BASE', '/accounts/')
    SAML2_DEFAULT_IDP = ENV.get('DJANGO_SAML2_DEFAULT_IDP', '')
    # Append the query parameter for idp to the default if it's set, otherwise do nothing
    if SAML2_DEFAULT_IDP:
        SAML2_DEFAULT_IDP = '?idp=%s' % SAML2_DEFAULT_IDP

    INSTALLED_APPS += ('djangosaml2',)
    AUTHENTICATION_BACKENDS += (
        'djangosaml2.backends.Saml2Backend',
    )
    LOGIN_URL = '%slogin/%s' % (SAML2_URL_PATH, SAML2_DEFAULT_IDP)
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    SAML2_FILES_BASE = ENV.get('SAML2_FILES_BASE', '/saml/')
    SAML2_REMOTE_METADATA = ENV.get('SAML2_REMOTE_METADATA', '')
    SAML2_REMOTE_PEM_FILE = ENV.get('SAML2_REMOTE_PEM_FILE', '')

    SAML_CONFIG = {
        'xmlsec_binary': '/usr/bin/xmlsec1',
        'entityid': '%smetadata/' % SAML2_URL_BASE,

        # directory with attribute mapping
        # 'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),
        'name': 'Student Dashboard',
        # this block states what services we provide
        'service': {
            # we are just a lonely SP
            'sp': {
                'name': 'Student Dashboard',
                'name_id_format': ('urn:oasis:names:tc:SAML:2.0:'
                                   'nameid-format:transient'),
                'authn_requests_signed': 'true',
                'allow_unsolicited': True,
                'endpoints': {
                    # url and binding to the assetion consumer service view
                    # do not change the binding or service name
                    'assertion_consumer_service': [
                        ('%sacs/' % SAML2_URL_BASE, saml2.BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view+

                    # do not change the binding or service name
                    'single_logout_service': [
                        ('%sls/' % SAML2_URL_BASE, saml2.BINDING_HTTP_REDIRECT),
                        ('%sls/post' % SAML2_URL_BASE, saml2.BINDING_HTTP_POST),
                    ],
                },

                # attributes that this project need to identify a user
                'required_attributes': ['uid'],

                # attributes that may be useful to have but not required
                'optional_attributes': ['eduPersonAffiliation'],
            },
        },

        # where the remote metadata is stored
        'metadata': [{
            "class": "saml2.mdstore.MetaDataExtern",
            "metadata": [
                (SAML2_REMOTE_METADATA, SAML2_REMOTE_PEM_FILE)]
            }
        ],

        # set to 1 to output debugging information
        'debug': DEBUG,

        # certificate
        'key_file': os.path.join(SAML2_FILES_BASE, 'student-dashboard-saml.key'),  'cert_file': os.path.join(SAML2_FILES_BASE, 'student-dashboard-saml.pem'),
    }

    ACS_DEFAULT_REDIRECT_URL = ENV.get('DJANGO_ACS_DEFAULT_REDIRECT', '/')
    LOGIN_REDIRECT_URL = ENV.get('DJANGO_LOGIN_REDIRECT_URL', '/')

    LOGOUT_REDIRECT_URL = ENV.get('DJANGO_LOGOUT_REDIRECT_URL', '/')

    SAML_CREATE_UNKNOWN_USER = True

    SAML_ATTRIBUTE_MAPPING = {
        'uid': ('username', ),
        'mail': ('email', ),
        'givenName': ('first_name', ),
        'sn': ('last_name', ),
    }
else:
    AUTHENTICATION_BACKENDS += ('django.contrib.auth.backends.ModelBackend',)
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL='/'

# Give an opportunity to disable LTI
if ENV.get('STUDENT_DASHBOARD_LTI', False):
    INSTALLED_APPS += ('django_lti_auth',)
    if not 'django.contrib.auth.backends.ModelBackend' in AUTHENTICATION_BACKENDS:
        AUTHENTICATION_BACKENDS += ('django.contrib.auth.backends.ModelBackend',)

    PYLTI_CONFIG = {
        "consumers": ENV.get("PYLTI_CONFIG_CONSUMERS", {}),
        "method_hooks":{
            "valid_lti_request": "dashboard.lti.valid_lti_request",
            "invalid_lti_request": "dashboard.lti.invalid_lti_request"
        },
        "next_url": "home"
    }
    LTI_PERSON_SOURCED_ID_FIELD = ENV.get('LTI_PERSON_SOURCED_ID_FIELD',
        "custom_canvas_user_login_id")
    LTI_EMAIL_FIELD = ENV.get('LTI_EMAIL_FIELD',
        "lis_person_contact_email_primary")
    LTI_CANVAS_COURSE_ID_FIELD = ENV.get('LTI_CANVAS_COURSE_ID_FIELD',
        "custom_canvas_course_id")
    LTI_FIRST_NAME = ENV.get('LTI_FIRST_NAME',
        "lis_person_name_given")
    LTI_LAST_NAME = ENV.get('LTI_LAST_NAME',
        "lis_person_name_family")
    
# controls whether Unizin specific features/data is available from the Canvas Data source
DATA_WAREHOUSE_IS_UNIZIN = ENV.get("DATA_WAREHOUSE_IS_UNIZIN", True)

# This is used to fix ids from Canvas Data which are incremented by some large number
CANVAS_DATA_ID_INCREMENT = ENV.get("CANVAS_DATA_ID_INCREMENT", 17700000000000000)

# Allow enabling/disabling the View options globally
VIEWS_DISABLED = ENV.get('VIEWS_DISABLED', [])

# Time to run cron
RUN_AT_TIMES = ENV.get('RUN_AT_TIMES', [])

# Add any settings you need to be available to templates in this array
SETTINGS_EXPORT = ['LOGIN_URL','LOGOUT_URL','DEBUG', 'GA_ID', 'RESOURCE_VALUES']

# Method to show the user, if they're authenticated and superuser
def show_debug_toolbar(request):
    return DEBUG and request.user and request.user.is_authenticated and request.user.is_superuser

DEBUG_TOOLBAR_PANELS = dt_settings.PANELS_DEFAULTS

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_debug_toolbar,
}

# Number of weeks max to allow by default. some begin/end dates in Canvas aren't correct
MAX_DEFAULT_WEEKS = ENV.get("MAX_DEFAULT_WEEKS", 16)

CLIENT_CACHE_TIME = ENV.get("CLIENT_CACHE_TIME", 3600)

CRON_BQ_IN_LIMIT = ENV.get("CRON_BQ_IN_LIMIT", 20)

CANVAS_FILE_PREFIX = ENV.get("CANVAS_FILE_PREFIX", "")
CANVAS_FILE_POSTFIX = ENV.get("CANVAS_FILE_POSTFIX", "")

# strings for construct file download url

CANVAS_FILE_ID_NAME_SEPARATOR = "|"

RESOURCE_ACCESS_CONFIG = ENV.get("RESOURCE_ACCESS_CONFIG", {})

# Git info settings
SHA_ABBREV_LENGTH = 7

# Django CSP Settings, load up from file if set
if "CSP" in ENV:
    MIDDLEWARE += ['csp.middleware.CSPMiddleware',]
    for csp_key, csp_val in ENV.get("CSP").items():
        # If there's a value set for this CSP config, set it as a global
        if (csp_val):
            globals()["CSP_"+csp_key] = csp_val
# If CSP not set, add in XFrameOptionsMiddleware
else:
    MIDDLEWARE += ['django.middleware.clickjacking.XFrameOptionsMiddleware',]

# These are mostly needed by Canvas but it should also be in on general 
CSRF_COOKIE_SECURE = ENV.get("CSRF_COOKIE_SECURE", False)
if CSRF_COOKIE_SECURE:
    CSRF_TRUSTED_ORIGINS = ENV.get("CSRF_TRUSTED_ORIGINS", [])
    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# When using the application with iframes (e.g. with LTI), these need to be set to None. However, we'll need to update
# this when new browser versions expect (and the Django version allows) the string "None".
SESSION_COOKIE_SAMESITE = ENV.get("SESSION_COOKIE_SAMESITE", None)
CSRF_COOKIE_SAMESITE = ENV.get("CSRF_COOKIE_SAMESITE", None)

# IMPORT LOCAL ENV
# =====================
try:
    from settings_local import *
except ImportError:
    pass
