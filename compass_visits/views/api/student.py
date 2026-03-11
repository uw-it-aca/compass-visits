# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from userservice.user import UserService
from compass_visits.dao.visit_dao import (get_active_visit_for_student,
                                          get_total_minutes_by_netid,
                                          get_student_state)
from compass_visits.views.api import RESTDispatchLogin


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
        mock_profile = {
            "netid": netid,
            "student_name": "James Average",
            "photo_url": "https://example.com/photo.jpg",
            "total_minutes": get_total_minutes_by_netid(netid),
            "current_state": get_student_state(active_visit),
            "visit": active_visit.json_data() if active_visit else None
        }
        return self.json_response(status=200, content=mock_profile)
