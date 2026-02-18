# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from compass_visits.dao.auth import validate_token
from functools import wraps


def token_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            validate_token(token)
        except Exception as e:
            kwargs['error'] = str(e)
        return func(request, *args, **kwargs)
    return wrapper
