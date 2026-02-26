# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.views.api import RESTDispatchLogin
from compass_visits.dao.visit_options import get_visit_options


class VisitOptions(RESTDispatchLogin):
    """
    API view for retrieving visit options.

    Methods
    -------
    get(request, *args, **kwargs)
        Handles GET requests and returns available visit options as a JSON
        response.

    Returns
    -------
    JsonResponse
        A JSON response with status 200 containing the visit options.
    """
    def get(self, request, *args, **kwargs):
        options = get_visit_options()
        return self.json_response(status=200, content=options)
