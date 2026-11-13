# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core.exceptions import DataFailureException
from userservice.user import UserService

from compass_visits.dao.pws import get_regid_by_netid
from compass_visits.dao.visit_options import get_visit_options
from compass_visits.views.api import RESTDispatchLogin


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
        try:
            netid = UserService().get_user()
            regid = get_regid_by_netid(netid)
            options = get_visit_options(regid)
            return self.json_response(status=200, content=options)
        except DataFailureException as e:
            return self.json_response(status=500, content={'error': str(e)})
