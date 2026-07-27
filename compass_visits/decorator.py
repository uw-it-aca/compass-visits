# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from functools import wraps

from compass_visits.dao.auth import validate_token


def token_required(func):
    """
    Decorator that ensures a valid authentication token is in the request.

    Args:
        func (callable): The view function to be decorated.

    Returns:
        callable: The wrapped function that checks for a valid token
                  before execution.

    Raises:
        Passes any exception raised by `validate_token` as an 'error'
        keyword argument to the wrapped function.

    Notes:
        - Expects the token to be provided in the 'HTTP_AUTHORIZATION'
            header of the request.
        - If token validation fails, the error message is added to the
            function's keyword arguments as 'error'.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            validate_token(token)
        except Exception as e:
            kwargs['error'] = str(e)
        return func(request, *args, **kwargs)
    return wrapper
