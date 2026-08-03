import os

from .base_settings import *

INSTALLED_APPS += [
    'compass_visits.apps.CompassVisitsConfig',
    'compass_visits.apps.ViteStaticFilesConfig',
    'userservice',
    'supporttools',
    "rc_django",
    "persistent_message",
]

INSTALLED_APPS.remove('django.contrib.staticfiles')

# If you have file data, define the path here
# DATA_ROOT = os.path.join(BASE_DIR, 'compass_visits/data')

GOOGLE_ANALYTICS_KEY = os.getenv('GOOGLE_ANALYTICS_KEY', default=' ')

MIDDLEWARE += [
    "userservice.user.UserServiceMiddleware",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "supporttools.context_processors.supportools_globals",
                "supporttools.context_processors.has_less_compiled",
                'compass_visits.context_processors.google_analytics',
                'compass_visits.context_processors.django_debug',
            ],
        },
    }
]


SUPPORTTOOLS_PARENT_APP = "Compass Visits"
SUPPORTTOOLS_PARENT_APP_URL = "/"

# Compass Visits -> Compass restclient settings used by dao/compass.py.
RESTCLIENTS_COMPASS_DAO_CLASS = os.getenv(
    'RESTCLIENTS_COMPASS_DAO_CLASS', 'Live')
RESTCLIENTS_COMPASS_HOST = os.getenv(
    'RESTCLIENTS_COMPASS_HOST', 'http://compass_app:8000')
RESTCLIENTS_COMPASS_AUTH_TOKEN = os.getenv(
    'RESTCLIENTS_COMPASS_AUTH_TOKEN', os.getenv('COMPASS_AUTH_TOKEN', 'testtoken'))

USERSERVICE_OVERRIDE_AUTH_MODULE = "compass_visits.dao.auth.is_admin_user"
RESTCLIENTS_ADMIN_AUTH_MODULE = "compass_visits.dao.auth.can_proxy_restclients"
PERSISTENT_MESSAGE_AUTH_MODULE = (
    "compass_visits.dao.auth.is_admin_user"
)

# ENV specific settings
if os.getenv('ENV') == 'localdev':
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True
    VITE_MANIFEST_PATH = os.path.join(
        BASE_DIR, 'compass_visits', 'static', '.vite', 'manifest.json'
    )
    MOCK_SAML_ATTRIBUTES = {
        "uwnetid": ["javerage"],
        "affiliations": ["student", "member"],
        "eppn": ["javerage@uw.edu"],
        "scopedAffiliations": [
            "student@washington.edu",
            "member@washington.edu",
        ],
        "isMemberOf": ["u_test_group"],
        "displayName": ["James Average"],
        "preferredFirst": ["James"],
        "preferredSurname": ["Average"],
    }
    ADMIN_GROUP = "u_test_group"
    SUPPORT_GROUP = "u_test_group"
    EXTERNAL_API_TOKEN = "testtoken"

if os.getenv('ENV') == 'localdev' or os.getenv('ENV') == 'test':
    ALLOW_USER_OVERRIDE_FOR_WRITE = True

if os.getenv('ENV') == 'test' or os.getenv('ENV') == 'prod':
    VITE_MANIFEST_PATH = os.path.join(
        os.sep, 'static', '.vite', 'manifest.json')
    EXTERNAL_API_TOKEN = os.getenv('EXTERNAL_API_TOKEN')
    SUPPORT_GROUP = os.getenv('SUPPORT_GROUP')
    ADMIN_GROUP = os.getenv('ADMIN_GROUP')
    RESTCLIENTS_COMPASS_AUTH_TOKEN = os.getenv(
        'RESTCLIENTS_COMPASS_AUTH_TOKEN', "")
    RESTCLIENTS_COMPASS_DAO_CLASS = "Live"
    RESTCLIENTS_COMPASS_HOST = os.getenv(
    'RESTCLIENTS_COMPASS_HOST', "")
    RESTCLIENTS_COMPASS_AUTH_TOKEN = os.getenv(
        'RESTCLIENTS_COMPASS_AUTH_TOKEN', )

if os.getenv('ENV') == 'prod':
    ALLOW_USER_OVERRIDE_FOR_WRITE = False
