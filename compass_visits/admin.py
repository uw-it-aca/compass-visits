# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.models import (ProgramArea,
                                   TutoringOption,
                                   WritingService,
                                   Visit)
from compass_visits.dao.auth import is_admin_user
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
import pprint


class SAMLAdminSite(admin.AdminSite):
    site_header = 'Compass admin'

    def __init__(self, *args, **kwargs):
        super(SAMLAdminSite, self).__init__(*args, **kwargs)
        self._registry.update(admin.site._registry)

    def has_permission(self, request):
        return is_admin_user(request)

    def login(self, request, extra_context=None):
        if self.has_permission(request):
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)
        else:
            return HttpResponseRedirect('/not-authorized/')


class AbstractSAMLAdminModel():
    def has_add_permission(self, request):
        return is_admin_user(request)

    def has_change_permission(self, request, obj=None):
        return is_admin_user(request)

    def has_delete_permission(self, request, obj=None):
        return is_admin_user(request)

    def has_module_permission(self, request):
        return is_admin_user(request)


class SAMLAdminModel(AbstractSAMLAdminModel, admin.ModelAdmin):
    pass

class VisitAdminModel(AbstractSAMLAdminModel, admin.ModelAdmin):
    list_display = ('student_netid', 'program_area__name', 'tutoring_option__name',
                    'writing_service__name', 'course', 'check_in_date',
                    'check_out_date', 'is_verified')


admin_site = SAMLAdminSite(name='SAMLAdmin')
admin_site.register(ProgramArea, SAMLAdminModel)
admin_site.register(TutoringOption, SAMLAdminModel)
admin_site.register(WritingService, SAMLAdminModel)
admin_site.register(Visit, VisitAdminModel)
