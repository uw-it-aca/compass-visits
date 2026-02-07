# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.views.api import RESTDispatch
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
    def post(self, request, *args, **kwargs):
        # TODO: implement this method to create a new visit
        return self.json_response(status=200, content={})


class VisitDetailView(RESTDispatch):
    def patch(self, request, visit_id, *args, **kwargs):
        request_body = json.loads(request.body)
        if request_body.get('verify', False):
            # TODO: mark visit verified
            pass
        if request_body.get('checkout', False):
            # TODO: mark visit checked out
            pass
        return self.json_response(status=200, content={})

    def delete(self, request, visit_id, *args, **kwargs):
        # TODO: implement this method to delete a visit
        return self.json_response(status=200, content={})


class CompassStudentVisits(RESTDispatch):
    def get(self, request, student_netid, *args, **kwargs):
        # TODO: Take a student's netid and return a list of their visits,
        #  sorted by date
        return self.json_response(status=200, content=[])
