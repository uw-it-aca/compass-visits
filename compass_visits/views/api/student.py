
# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.views.api import RESTDispatch
import json


class StudentProfileView(RESTDispatch):
    def get(self, request, *args, **kwargs):
        # TODO return student profile information
        return self.json_response(status=200, content={})
