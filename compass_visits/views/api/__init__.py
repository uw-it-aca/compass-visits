# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.views import View
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from compass_visits.decorator import token_required


class RESTDispatch(View):
    """
    RESTDispatch provides static methods for returning JSON HTTP responses in
    Django views.

    Methods
    -------
    json_response(content={}, status=200):
        Serializes the given content to JSON and returns an HttpResponse
        with the specified status code.
        If serialization fails, returns a 400 error response.

    error_response(status, message='', content={}):
        Returns an HttpResponse with the given status code and a JSON body
        containing an error message.
    """
    @staticmethod
    def json_response(content={}, status=200):
        try:
            data = json.dumps(content,
                              sort_keys=True,
                              cls=DjangoJSONEncoder)
            return HttpResponse(data,
                                status=status,
                                content_type='application/json')
        except TypeError:
            return RESTDispatch().error_response(400)

    @staticmethod
    def error_response(status, message='', content=None):
        if content is None:
            content = {}
        content['error'] = str(message)
        return HttpResponse(json.dumps(content),
                            status=status,
                            content_type='application/json',
                            )


class RESTDispatchLogin(RESTDispatch):
    """
    A RESTful dispatch view that requires user authentication.

    This class extends `RESTDispatch` and ensures that all incoming requests
    are authenticated using Django's `login_required` decorator. Any request
    to this view will be redirected to the login page if the user is not
    authenticated.

    Methods
    -------
    dispatch(*args, **kwargs)
        Handles the HTTP request and enforces authentication before delegating
        to the parent class's dispatch method.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class RESTDispatchToken(RESTDispatch):
    """
    A subclass of RESTDispatch that enforces token-based authentication on
    all requests.

    Methods
    -------
    dispatch(request, *args, **kwargs)
        Handles incoming HTTP requests. If an authentication error is
        present in kwargs, returns a 403 error response with the provided
        error message. Otherwise, delegates request handling to the parent
        class's dispatch method.

    Decorators
    ----------
        Ensures that the dispatch method requires a valid token.
    """
    @method_decorator(token_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('error'):
            return self.error_response(403, message=kwargs['error'])
        return super().dispatch(request, *args, **kwargs)
