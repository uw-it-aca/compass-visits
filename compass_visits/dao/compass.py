# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core.dao import DAO
from os.path import abspath, dirname
import os
import json
from restclients_core.exceptions import DataFailureException
from restclients_core import models
import datetime


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


class CompassVisits(object):
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
