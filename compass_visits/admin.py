# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from compass_visits.dao.auth import is_admin_user
from compass_visits.models import Visit, WritingService


class SAMLAdminSite(admin.AdminSite):
    site_header = 'Compass admin'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry.update(admin.site._registry)

    def has_permission(self, request):
        return is_admin_user(request)

    def login(self, request, extra_context=None):
        if self.has_permission(request):
            index_path = reverse('admin:index', current_app=self.name)
            return HttpResponseRedirect(index_path)
        else:
            return HttpResponseRedirect('/not-authorized/')


class AbstractSAMLAdminModel:
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
    list_display = ('id', 'student_syskey', 'program_area',
                    'tutoring_option',
                    'writing_service__name', 'course', 'check_in_date',
                    'check_out_date', 'is_verified')


admin_site = SAMLAdminSite(name='SAMLAdmin')
admin_site.register(WritingService, SAMLAdminModel)
admin_site.register(Visit, VisitAdminModel)
