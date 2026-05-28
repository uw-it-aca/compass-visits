# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.urls import re_path
from django.views.generic import TemplateView
from compass_visits.views.pages import DefaultPageView
from compass_visits.views.api.visit_student import (StudentVisitList,
                                                    VisitView,
                                                    VisitDetailView)
from compass_visits.views.api.options import VisitOptions
from compass_visits.views.api.student import StudentProfileView
from compass_visits.views.api.external.visit_external import (
    VisitAdminListView, CompassStudentVisitsView, ManageVisitsView)
from compass_visits.views.api.external.options_external import \
    VisitOptionsExternal
from compass_visits.admin import admin_site


# start with an empty url array
urlpatterns = []

# add debug routes for developing error pages
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^500$",
            TemplateView.as_view(template_name="500.html"),
            name="500_response",
        ),
        re_path(
            r"^404$",
            TemplateView.as_view(template_name="404.html"),
            name="404_response",
        ),
    ]

urlpatterns += [
    re_path(r"^admin", admin_site.urls),
    re_path(r'^api/internal/visit/(?P<visit_id>\d+)/$',
            VisitDetailView.as_view(),
            name="visit_detail"),
    re_path(r'^api/internal/visit/$',
            VisitView.as_view(),
            name="visit"),
    re_path(r'^api/internal/studentvisits/$',
            StudentVisitList.as_view(),
            name="student_visits"),
    re_path(r'^api/internal/profile/$',
            StudentProfileView.as_view(),
            name="student_profile"),
    re_path(r'^api/internal/visitoptions/$',
            VisitOptions.as_view(),
            name="visit_options"),
    re_path(r'^api/v1/visitadminlist/$',
            VisitAdminListView.as_view(),
            name="visit_admin_list"),
    re_path(r'^api/v1/visitoptions/(?P<student_regid>\w+)/$',
            VisitOptionsExternal.as_view(),
            name="visit_options_external"),
    re_path(r'^api/v1/studentvisits/(?P<student_syskey>\w+)/$',
            CompassStudentVisitsView.as_view(),
            name="compass_student_visits"),
    re_path(r'^api/v1/managevisit/(?P<visit_id>\d+)/$',
            ManageVisitsView.as_view(),
            name="manage_visit"),
    re_path(r'^api/v1/managevisit/$',
            ManageVisitsView.as_view(),
            name="manage_visits"),
    re_path(
        r"^(verify|checkout|create|summary).*$",
        DefaultPageView.as_view(),
        name="vue_router_page"),
    re_path(r"^$", DefaultPageView.as_view(), name="default_page"),
]
