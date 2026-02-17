# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.core.exceptions import PermissionDenied
from userservice.user import UserService
from compass_visits.exceptions import OverrideNotPermitted


def valid_user_override():
    if (not getattr(settings, "ALLOW_USER_OVERRIDE_FOR_WRITE", False) and
            UserService().get_override_user() is not None):
        raise OverrideNotPermitted()


def can_write_visit(visit_netid):
    if UserService().get_user() != visit_netid:
        raise PermissionDenied("User does not have permission to modify "
                               "this visit")
