# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core.dao import DAO
from os.path import abspath, dirname
import os
import json
from restclients_core.exceptions import DataFailureException
from restclients_core import models
import datetime
from django.utils.dateparse import parse_datetime


class COMPASS_DAO(DAO):
    def service_name(self):
        return 'compass'

    def service_mock_paths(self):
        path = [abspath(os.path.join(dirname(__file__), "resources"))]
        return path

    def _custom_headers(self, method, url, headers, body):
        custom_headers = {}
        token = self.get_service_setting('AUTH_TOKEN')
        if token:
            custom_headers['Authorization'] = "Token {}".format(token)
        return custom_headers


class Compass(object):
    """
    This class provides an interface to the compass visits web service.
    """

    API = '/api/v1'

    def __init__(self):
        self.dao = COMPASS_DAO()

    def get_ic_eligibility(self, syskey):
        """
        Returns IC eligibility for the given syskey.
        """
        url = "{}/visit/eligibility/{}".format(self.API, syskey)
        response = self.dao.getURL(url)
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error getting IC eligibility "
                                       "{}: {}".format(syskey,
                                                       response.status))
        data = json.loads(response.data)
        return data.get('eligible', False)

    def store_visit(self, visit):
        """
        Stores a visit in compass DB
        """
        url = "{}/visit/omad".format(self.API)
        response = self.dao.postURL(url, visit.json_data())

        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error storing visit:"
                                       "{}".format(response.status))
        return json.loads(response.data)

    def get_current_quarter_visits(self, syskey):
        """
        Returns a list of visits for the given syskey in the current quarter.
        """
        url = "{}/visit/external_student/{}".format(self.API, syskey)
        response = self.dao.getURL(url)
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error getting visits for syskey "
                                       "{}: {}".format(syskey,
                                                       response.status))
        data = json.loads(response.data)
        visits = []
        for visit in data:
            visit['checkin_date'] = parse_datetime(visit['checkin_date'])
            if visit.get('checkout_date'):
                visit['checkout_date'] = parse_datetime(visit['checkout_date'])
            visits.append(CompassVisitModel(**visit))
        return visits


class CompassVisitModel(models.Model):
    """
    This class represents a visit in compass.

    """
    student_netid = models.CharField()
    visit_type = models.CharField()
    course_code = models.CharField()
    tutoring_option = models.CharField()
    checkin_date = models.DateTimeField()
    checkout_date = models.DateTimeField()

    def json_data(self):
        return {
            "student_netid": self.student_netid,
            "visit_type": self.visit_type,
            "course_code": self.course_code,
            "tutoring_option": self.tutoring_option,
            "checkin_date": self.checkin_date.isoformat(),
            "checkout_date": self.checkout_date.isoformat()
        }

    def student_json_data(self):
        active_minutes = 0
        if self.checkout_date and self.checkin_date:
            active_minutes = int((self.checkout_date - self.checkin_date)
                                 .total_seconds() / 60)

        return {
            "student_netid": self.student_netid,
            "visit_type": self.visit_type,
            "course": self.course_code,
            "tutoring_option": self.tutoring_option,
            "check_in_date": self.checkin_date.isoformat(),
            "check_out_date": self.checkout_date.isoformat(),
            "active_minutes": active_minutes,
        }
