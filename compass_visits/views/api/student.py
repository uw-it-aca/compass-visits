# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from userservice.user import UserService
from compass_visits.dao.compass import Compass
from compass_visits.dao.visit_dao import (get_active_visit_for_student,
                                          get_total_minutes_by_syskey,
                                          get_student_state)
from compass_visits.dao.pws import get_student_profile, get_student_photo
from compass_visits.views.api import RESTDispatchLogin
from restclients_core.exceptions import DataFailureException
import base64


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

        netid = UserService().get_user()
        try:
            student_profile = get_student_profile(netid)
        except DataFailureException:
            return self.error_response(status=400,
                                       message="Unable to retrieve student "
                                               "information")
        try:
            photo_data = get_student_photo(student_profile.get('uwregid'))
            student_profile['photo'] = (base64
                                        .b64encode(photo_data.getvalue())
                                        .decode('ascii')) \
                if photo_data else None
        except DataFailureException:
            student_profile['photo'] = None

        student_syskey = student_profile.get('student_syskey')
        ic_elligible = False
        if student_syskey:
            try:
                ic_elligible = Compass().get_ic_eligibility(student_syskey)
            except DataFailureException:
                ic_elligible = False

        # TODO: Preserve legacy response key for compatibility; rename in next
        # major API version.
        student_profile['ic_elligible'] = ic_elligible

        if ic_elligible:
            active_visit = get_active_visit_for_student(student_syskey)
            student_profile.update({
                "total_minutes": get_total_minutes_by_syskey(student_syskey),
                "current_state": get_student_state(active_visit),
                "visit": active_visit.json_data() if active_visit else None
            })

        return self.json_response(status=200, content=student_profile)
