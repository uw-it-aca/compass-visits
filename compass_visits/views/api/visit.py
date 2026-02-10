# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from compass_visits.views.api import RESTDispatch
from compass_visits.dao.visit import validate_visit_data
from compass_visits.exceptions import ValidationError
from compass_visits.models import Visit
from userservice.user import UserService

import json


class StudentVisitList(RESTDispatch):
    def get(self, request, *args, **kwargs):
        # TODO: implement this method to return the list of visits for the user
        return self.json_response(status=200, content=[])


class VistAdminListView(RESTDispatch):
    def get(self, request, *args, **kwargs):
        # TODO: implement this method to return the list of visits for
        #  compass admin view
        return self.json_response(status=200, content=[])


class VisitView(RESTDispatch):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            student_netid = UserService().get_user()
            request_body = json.loads(request.body)
            validate_visit_data(request_body)
            visit = Visit.create_from_request(request_body, student_netid)
            return self.json_response(status=200, content=visit.json_data())
        except ValidationError as e:
            return self.error_response(status=400, message=e)


class VisitDetailView(RESTDispatch):
    def patch(self, request, visit_id, *args, **kwargs):
        request_body = json.loads(request.body)
        try:
            visit = Visit.objects.get(id=visit_id)
            visit.update_visit(request_body)
            return self.json_response(status=200, content=visit.json_data())
        except Visit.DoesNotExist:
            return self.error_response(status=404, message="Visit not found")

    def delete(self, request, visit_id, *args, **kwargs):
        # TODO: implement this method to delete a visit
        return self.json_response(status=200, content={})


class CompassStudentVisits(RESTDispatch):
    def get(self, request, student_netid, *args, **kwargs):
        # TODO: Take a student's netid and return a list of their visits,
        #  sorted by date
        return self.json_response(status=200, content=[])
