from .base_urls import *
from django.conf.urls import include
from django.urls import re_path

urlpatterns += [
    re_path(r'^', include('compass_visits.urls')),
    re_path(r'^support/?', include('userservice.urls')),
    re_path(r'^restclients/', include('rc_django.urls')),
    re_path(r'^persistent_message/', include('persistent_message.urls')),
    ]
