# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from userservice.user import UserService
from django.core.exceptions import ObjectDoesNotExist
from django.http import StreamingHttpResponse
from compass_visits.dao.visit_dao import (get_active_visit_for_student,
                                          get_total_minutes_by_netid,
                                          get_student_state)
from compass_visits.dao.pws import get_student_profile, get_student_photo
from compass_visits.views.api import RESTDispatchLogin
from restclients_core.exceptions import DataFailureException


class StudentProfileView(RESTDispatchLogin):
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve student information.

        Retrieves the current user's netid, fetches their active visit (if
        any), and constructs a profile containing student details such as
        name, photo URL, total hours, current state, and visit information.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse: A JSON response with status 200 containing the
                student's profile data.
        """
        # TODO Get student info from PDS
        netid = UserService().get_user()
        active_visit = get_active_visit_for_student(netid)
        mock_IC_elligible = True

        student_profile = get_student_profile(netid)

        student_profile['ic_elligible'] = mock_IC_elligible

        if mock_IC_elligible:
            student_profile.update({
                "total_minutes": get_total_minutes_by_netid(netid),
                "current_state": get_student_state(active_visit),
                "visit": active_visit.json_data() if active_visit else None
            })

        return self.json_response(status=200, content=student_profile)


class StudentPhotoView(RESTDispatchLogin):

    CACHE_TIME = 60 * 60 * 4  # Cache for 4 hours

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve the student's photo and return it.

        Retrieves the current user's netid, fetches their photo from PWS,
        and returns it in a JSON response.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse: A JSON response with status 200 containing the
                student's photo URL.
        """
        try:
            netid = UserService().get_user()
            photo = get_student_photo(netid)
            response = StreamingHttpResponse(photo, content_type='image/jpeg')
            response['Cache-Control'] = f'public,max-age={self.CACHE_TIME}'
            return response
        except (DataFailureException, ObjectDoesNotExist) as e:
            return self.json_response(status=getattr(e, 'status', 500),
                                      content={"error": str(e)})
