
# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from userservice.user import UserService
from compass_visits.dao.visit_dao import (get_active_visit_for_student,
                                          get_total_hours_by_netid,
                                          get_student_state)
from compass_visits.views.api import RESTDispatch


class StudentProfileView(RESTDispatch):
    def get(self, request, *args, **kwargs):
        # TODO Get student info from PDS
        netid = UserService().get_user()
        active_visit = get_active_visit_for_student(netid)
        mock_profile = {
            "netid": netid,
            "student_name": "James Average",
            "photo_url": "https://example.com/photo.jpg",
            "total_hours": get_total_hours_by_netid(netid),
            "current_state": get_student_state(active_visit),
            "visit": active_visit.json_data() if active_visit else None
        }
        return self.json_response(status=200, content=mock_profile)
