# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.views.api import RESTDispatch
from compass_visits.dao.visit_dao import (get_visits_pending_verification,
                                          get_visits_pending_checkout)


class VistAdminListView(RESTDispatch):
    def get(self, request, *args, **kwargs):
        pend_verif = [visit.json_data() for visit
                      in get_visits_pending_verification()]
        pend_check = [visit.json_data() for visit
                      in get_visits_pending_checkout()]
        response = {'pending_verification': pend_verif,
                    'pending_checkout': pend_check
                    }
        return self.json_response(status=200, content=response)


class CompassStudentVisits(RESTDispatch):
    def get(self, request, student_netid, *args, **kwargs):
        pass
