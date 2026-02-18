# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from compass_visits.models import Visit
from compass_visits.views.api import RESTDispatchToken
from compass_visits.exceptions import ValidationError
from compass_visits.dao.visit_dao import (get_visits_pending_verification,
                                          get_visits_pending_checkout,
                                          get_completed_visits_by_netid,
                                          manager_update_visit,
                                          manager_create_visit_from_request)


class VistAdminListView(RESTDispatchToken):
    def get(self, request, *args, **kwargs):
        pend_verif = [visit.json_data() for visit
                      in get_visits_pending_verification()]
        pend_check = [visit.json_data() for visit
                      in get_visits_pending_checkout()]
        response = {'pending_verification': pend_verif,
                    'pending_checkout': pend_check
                    }
        return self.json_response(status=200, content=response)


class CompassStudentVisitsView(RESTDispatchToken):
    def get(self, request, student_netid, *args, **kwargs):
        visits = get_completed_visits_by_netid(student_netid)
        visit_list = [visit.json_data() for visit in visits]
        return self.json_response(status=200, content=visit_list)


class ManageVisitsView(RESTDispatchToken):
    def patch(self, request, visit_id, *args, **kwargs):
        request_body = json.loads(request.body)
        try:
            visit = Visit.objects.get(id=visit_id)
            manager_update_visit(visit, request_body)
            return self.json_response(status=200, content=visit.json_data())
        except Visit.DoesNotExist:
            return self.error_response(status=404, message="Visit not found")
        except ValidationError as e:
            return self.error_response(status=400, message=e)

    def post(self, request, *args, **kwargs):
        request_body = json.loads(request.body)
        try:
            visit = manager_create_visit_from_request(request_body)
            return self.json_response(status=200, content=visit.json_data())
        except ValidationError as e:
            return self.error_response(status=400, message=e)

    def delete(self, request, visit_id, *args, **kwargs):
        try:
            visit = Visit.objects.get(id=visit_id)
            visit.delete()
            return self.json_response(status=200, content={})
        except Visit.DoesNotExist:
            return self.error_response(status=404, message="Visit not found")
