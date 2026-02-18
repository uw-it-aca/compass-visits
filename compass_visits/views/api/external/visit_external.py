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


class VisitAdminListView(RESTDispatchToken):
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve visits pending verification and
        checkout.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response containing two lists:
                - 'pending_verification': Visits pending verification.
                - 'pending_checkout': Visits pending checkout.
            Each visit is represented as a JSON-serializable dictionary.
        """
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
        """
        Handles GET requests to retrieve completed visits for a given student.

        Args:
            request: The HTTP request object.
            student_netid (str): The NetID of the student whose visits are
                being requested.

        Returns:
            JsonResponse: A JSON response containing a list of completed
                visits for the specified student.
        """
        visits = get_completed_visits_by_netid(student_netid)
        visit_list = [visit.json_data() for visit in visits]
        return self.json_response(status=200, content=visit_list)


class ManageVisitsView(RESTDispatchToken):
    def patch(self, request, visit_id, *args, **kwargs):
        """
        Partially updates a Visit instance with the provided data.

        Args:
            request (HttpRequest): The HTTP request object containing the
                PATCH data in JSON format.
            visit_id (int): The ID of the Visit to update.

        Returns:
            JsonResponse: A JSON response with the updated Visit data and a
                200 status code if successful.
            JsonResponse: A JSON response with a 404 status code if the Visit
                does not exist.
            JsonResponse: A JSON response with a 400 status code if the
                provided data is invalid.
        """
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
        """
        Handles POST requests to create a new visit from the provided request
        body. Allows managers to create visits on behalf of students and
        enables setting validation and check out status through the request
        data.

        Args:
            request: The HTTP request object containing the JSON payload.

        Returns:
            JsonResponse: A JSON response with the created visit data and
                status 200 on success.
            JsonResponse: An error response with status 400 and validation
                error message on failure.
        """
        request_body = json.loads(request.body)
        try:
            visit = manager_create_visit_from_request(request_body)
            return self.json_response(status=200, content=visit.json_data())
        except ValidationError as e:
            return self.error_response(status=400, message=e)

    def delete(self, request, visit_id, *args, **kwargs):
        """
        Deletes a Visit instance with the specified visit_id.

        Args:
            request: The HTTP request object.
            visit_id (int): The ID of the Visit to be deleted.

        Returns:
            JsonResponse: An empty JSON response with status 200 if deletion
                is successful.
            JsonResponse: An error response with status 404 if the Visit does
                not exist.
        """
        try:
            visit = Visit.objects.get(id=visit_id)
            visit.delete()
            return self.json_response(status=200, content={})
        except Visit.DoesNotExist:
            return self.error_response(status=404, message="Visit not found")
