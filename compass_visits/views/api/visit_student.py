# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json

from django.core.exceptions import PermissionDenied
from restclients_core.exceptions import DataFailureException
from userservice.user import UserService

from compass_visits.dao.auth import can_write_visit, valid_user_override
from compass_visits.dao.pws import get_syskey_by_netid
from compass_visits.dao.visit_dao import (
    checkout_active_verified_visit,
    create_visit_from_request,
    get_current_quarter_visits_by_syskey,
    student_update_visit,
)
from compass_visits.exceptions import OverrideNotPermitted, ValidationError
from compass_visits.models import Visit
from compass_visits.views.api import RESTDispatchLogin


class StudentVisitList(RESTDispatchLogin):
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve a list of visits for the current
        student.

        Retrieves the current student's NetID using the UserService, fetches
        all Visit objects associated with that NetID, orders them by
        check-in date in descending order, serializes each visit to JSON,
        and returns the list as a JSON response.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response containing a list of the student's
                visits.
        """

        student_netid = UserService().get_user()
        try:
            student_syskey = get_syskey_by_netid(student_netid)
        except DataFailureException:
            return self.error_response(status=400,
                                       message="Unable to retrieve student "
                                               "information")
        try:
            visits = get_current_quarter_visits_by_syskey(student_syskey)
        except DataFailureException:
            return self.error_response(status=400,
                                       message="Unable to retrieve student "
                                               "information")
        for visit in visits:
            visit.student_netid = student_netid
        visit_list = [visit.student_json_data() for visit in visits]
        return self.json_response(status=200, content=visit_list)


class VisitView(RESTDispatchLogin):
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new visit for a student.

        Attempts to:
        - Validate user override permissions.
        - Retrieve the current student's NetID.
        - Parse the request body as JSON.
        - If a verified visit is in progress it will check out that visit and
            create a new, verified visit with the new request data. Handles
            the "switch" use case
        - Create a visit record using the request data and student NetID.
        - Return a JSON response with the created visit data on success.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: On success, returns a 200 response with visit data.
            JsonResponse: On validation error, returns a 400 response with
                error details.
            JsonResponse: If override is not permitted, returns a 403 response
                with error message.
        """
        try:
            valid_user_override()
            student_netid = UserService().get_user()
            student_syskey = get_syskey_by_netid(student_netid)
            switch_visit = checkout_active_verified_visit(student_syskey)
            request_body = json.loads(request.body)
            visit = create_visit_from_request(request_body,
                                              student_syskey,
                                              student_netid,
                                              verified=switch_visit)
            return self.json_response(status=200, content=visit.json_data())
        except ValidationError as e:
            return self.error_response(status=400, message=e)
        except OverrideNotPermitted as e:
            return self.error_response(status=403, message=e)
        except json.JSONDecodeError:
            return self.error_response(status=400,
                                       message="Invalid JSON format")
        except DataFailureException:
            return self.error_response(status=400,
                                       message="Unable to retrieve student "
                                               "information")


class VisitDetailView(RESTDispatchLogin):
    def patch(self, request, visit_id, *args, **kwargs):
        """
        Handles HTTP PATCH requests to update a Visit instance for a student.

        Args:
            request: The HTTP request object containing the PATCH data in
                visit = Visit.objects.select_related('writing_service').get(

        Returns:
            JsonResponse: A JSON response with the updated Visit data and HTTP
                200 status on success.
            JsonResponse: A JSON error response with HTTP 404 status if the
                Visit is not found.
            JsonResponse: A JSON error response with HTTP 400 status if
                validation fails.
            JsonResponse: A JSON error response with HTTP 403 status if
                the user lacks permission.
        """
        try:
            request_body = json.loads(request.body)
        except json.JSONDecodeError:
            return self.error_response(status=400,
                                       message="Invalid JSON format")
        try:
            visit = Visit.objects.select_related('writing_service').get(
                    id=visit_id)
            valid_user_override()
            can_write_visit(visit.student_syskey)
            student_update_visit(visit, request_body)
            return self.json_response(status=200, content=visit.json_data())
        except Visit.DoesNotExist:
            return self.error_response(status=404, message="Visit not found")
        except ValidationError as e:
            return self.error_response(status=400, message=e)
        except (OverrideNotPermitted, PermissionDenied) as e:
            return self.error_response(status=403, message=e)

    def delete(self, request, visit_id, *args, **kwargs):
        """
        Deletes a Visit instance specified by visit_id.

        Args:
            request: The HTTP request object.
            visit_id (int): The ID of the Visit to delete.

        Returns:
            JsonResponse: A JSON response with status 200 if deletion is
                          successful, 404 if the Visit does not exist,
                          or 403 if the user does not have permission.

        """
        try:
            visit = Visit.objects.get(id=visit_id)
            valid_user_override()
            can_write_visit(visit.student_syskey)
            visit.delete()
            return self.json_response(status=200, content={})
        except Visit.DoesNotExist:
            return self.error_response(status=404, message="Visit not found")
        except (OverrideNotPermitted, PermissionDenied) as e:
            return self.error_response(status=403, message=e)
