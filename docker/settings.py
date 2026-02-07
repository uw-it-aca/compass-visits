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
    VITE_MANIFEST_PATH = os.path.join(
        BASE_DIR, 'compass_visits', 'static', '.vite', 'manifest.json'
    )
else:
    VITE_MANIFEST_PATH = os.path.join(os.sep, 'static', '.vite', 'manifest.json')
