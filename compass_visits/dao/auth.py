# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.crypto import constant_time_compare
from userservice.user import UserService
from compass_visits.exceptions import OverrideNotPermitted


def valid_user_override():
    """
    Checks if user override is permitted for write operations.  By default,
    user override is not allowed for write operations unless the
    ALLOW_USER_OVERRIDE_FOR_WRITE setting is set to True.

    Raises:
        OverrideNotPermitted: If user override is not allowed and an
                              override user is set.
    """
    if (not getattr(settings, "ALLOW_USER_OVERRIDE_FOR_WRITE", False) and
            UserService().get_override_user() is not None):
        raise OverrideNotPermitted()


def can_write_visit(visit_netid):
    """
    Checks if the currently authenticated user matches the provided visit
    NetID.

    Args:
        visit_netid (str): The NetID of the visit owner.

    Raises:
        PermissionDenied: If the current user does not match the visit owner.
    """
    if UserService().get_user() != visit_netid:
        raise PermissionDenied("User does not have permission to modify "
                               "this visit")


def validate_token(token):
    """
    Validates the provided API token against the expected format and value.

    Args:
        token (str): The API token string to validate. Expected to start
                     with 'Token '.

    Raises:
        PermissionDenied: If the token is missing, has an invalid format,
                          or does not match the expected value from
                          settings.EXTERNAL_API_TOKEN.
    """
    TOKEN_PREFIX = "Token "
    if token is None:
        raise PermissionDenied("API token is required")
    if not token.startswith(TOKEN_PREFIX):
        raise PermissionDenied("Invalid API token format")
    token_value = token[len(TOKEN_PREFIX):]
    set_token = getattr(settings, "EXTERNAL_API_TOKEN", None)
    if set_token is None or not constant_time_compare(token_value, set_token):
        raise PermissionDenied("Invalid API token")
