# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.views.api import RESTDispatchLogin
from compass_visits.dao.visit_dao import (create_visit_from_request,
                                          student_update_visit)
from compass_visits.exceptions import ValidationError, OverrideNotPermitted
from compass_visits.models import Visit
from compass_visits.dao.auth import valid_user_override, can_write_visit
from django.core.exceptions import PermissionDenied
from userservice.user import UserService
import json


class StudentVisitList(RESTDispatchLogin):
    def get(self, request, *args, **kwargs):
        student_netid = UserService().get_user()
        visits = Visit.objects.filter(student_netid=student_netid).order_by(
            '-check_in_date')
        visit_list = [visit.json_data() for visit in visits]
        return self.json_response(status=200, content=visit_list)


class VisitView(RESTDispatchLogin):
    def post(self, request, *args, **kwargs):
        try:
            valid_user_override()
            student_netid = UserService().get_user()
            request_body = json.loads(request.body)
            visit = create_visit_from_request(request_body, student_netid)
            return self.json_response(status=200, content=visit.json_data())
        except ValidationError as e:
            return self.error_response(status=400, message=e)
        except OverrideNotPermitted as e:
            return self.error_response(status=403, message=str(e))


class VisitDetailView(RESTDispatchLogin):
    def patch(self, request, visit_id, *args, **kwargs):
        request_body = json.loads(request.body)
        try:
            visit = Visit.objects.get(id=visit_id)
            valid_user_override()
            can_write_visit(visit.student_netid)
            student_update_visit(visit, request_body)
            return self.json_response(status=200, content=visit.json_data())
        except Visit.DoesNotExist:
            return self.error_response(status=404, message="Visit not found")
        except ValidationError as e:
            return self.error_response(status=400, message=e)
        except (OverrideNotPermitted, PermissionDenied) as e:
            return self.error_response(status=403, message=str(e))

    def delete(self, request, visit_id, *args, **kwargs):
        try:
            visit = Visit.objects.get(id=visit_id)
            valid_user_override()
            can_write_visit(visit.student_netid)
            visit.delete()
            return self.json_response(status=200, content={})
        except Visit.DoesNotExist:
            return self.error_response(status=404, message="Visit not found")
        except (OverrideNotPermitted, PermissionDenied) as e:
            return self.error_response(status=403, message=str(e))
