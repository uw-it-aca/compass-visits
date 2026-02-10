from .base_settings import *

INSTALLED_APPS += [
    'compass_visits.apps.CompassVisitsConfig',
    'compass_visits.apps.ViteStaticFilesConfig',
    'userservice'
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
                'compass_visits.context_processors.google_analytics',
                'compass_visits.context_processors.django_debug',
                'compass_visits.context_processors.auth_user',
            ],
        },
    }
]

if os.getenv('ENV') == 'localdev':
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True
    VITE_MANIFEST_PATH = os.path.join(
        BASE_DIR, 'compass_visits', 'static', '.vite', 'manifest.json'
    )
    MOCK_SAML_ATTRIBUTES = {
        "uwnetid": ["javerage"],
        "uwregid": ["9136CCB8F66711D5BE060004AC494FFE"],
        "uwStudentSystemKey": ["000083856"],
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
else:
    VITE_MANIFEST_PATH = os.path.join(os.sep, 'static', '.vite', 'manifest.json')
