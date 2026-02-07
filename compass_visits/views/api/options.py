# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.views.api import RESTDispatch


class VisitOptions(RESTDispatch):
    def get(self, request, *args, **kwargs):
        # TODO: implement this method to return the list of
        #  program areas, tutoring options, and writing services
        return self.json_response(status=200, content=[])
