# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core.exceptions import DataFailureException

from compass_visits.dao.visit_options import get_visit_options
from compass_visits.views.api import RESTDispatchToken


class VisitOptionsExternal(RESTDispatchToken):
    """
    API view for retrieving visit options for admin users

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
    def get(self, request, student_regid, *args, **kwargs):
        try:
            options = get_visit_options(student_regid)
            return self.json_response(status=200, content=options)
        except DataFailureException as e:
            return self.json_response(status=500, content={'error': str(e)})
