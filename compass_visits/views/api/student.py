
# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from userservice.user import UserService
from compass_visits.dao.visit import (get_active_visit_for_student,
                                      get_total_hours_by_netid)
from compass_visits.views.api import RESTDispatch


class StudentProfileView(RESTDispatch):
    def get(self, request, *args, **kwargs):
        # TODO return student profile information
        netid = "javerage"
        mock_profile = {
            "netid": netid,
            "student_name": "James Average",
            "photo_url": "https://example.com/photo.jpg",
            "total_hours": get_total_hours_by_netid(netid)
        }
        return self.json_response(status=200, content={})


class StudentStateView(RESTDispatch):
    def get(self, request, *args, **kwargs):
        student_netid = UserService().get_acting_user()
        active_visit = get_active_visit_for_student(student_netid)
        state = "none"
        if active_visit is not None:
            if not active_visit.is_verified:
                state = "pending_verification"
            elif active_visit.check_out_date is None:
                state = "active"
            else:
                state = "none"

        response = {"state": state}
        if active_visit is not None:
            response["visit"] = active_visit.json_data()
        return self.json_response(status=200, content=response)
