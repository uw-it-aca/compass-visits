# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.views.api import RESTDispatch
from compass_visits.dao.visit_options import get_visit_options


class VisitOptions(RESTDispatch):
    def get(self, request, *args, **kwargs):
        options = get_visit_options()
        return self.json_response(status=200, content=options)
