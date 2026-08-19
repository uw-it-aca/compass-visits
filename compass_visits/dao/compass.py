# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
import os
from os.path import abspath, dirname

from django.utils.dateparse import parse_datetime
from restclients_core import models
from restclients_core.dao import DAO
from restclients_core.exceptions import DataFailureException


class COMPASS_DAO(DAO):
    def service_name(self):
        return 'compass'

    def service_mock_paths(self):
        path = [abspath(os.path.join(dirname(__file__), "..", "resources"))]
        return path

    def _custom_headers(self, method, url, headers, body):
        custom_headers = {}
        custom_headers['Content-Type'] = 'application/json'
        token = self.get_service_setting('AUTH_TOKEN')
        if token:
            custom_headers['Authorization'] = f"Token {token}"
        return custom_headers


class Compass:
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
        url = f"{self.API}/visit/eligibility/{syskey}/"
        response = self.dao.getURL(url)
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error getting IC eligibility "
                                       f"{syskey}: {response.status}")
        data = json.loads(response.data)
        return data.get('eligible', False)

    def get_visit_catalog(self):
        """Return the Compass-owned OMAD visit catalog."""
        url = f"{self.API}/visit/catalog"
        response = self.dao.getURL(url)
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error getting visit catalog: "
                                       f"{response.status}")
        return json.loads(response.data)

    def store_visit(self, visit):
        """
        Stores a visit in compass DB
        """
        url = f"{self.API}/visit/omad"
        response = self.dao.postURL(url, body=json.dumps(visit.json_data()))
        response_data = response.data.decode(
            "utf-8", errors="replace"
        ) if isinstance(response.data, bytes) else (response.data or "")

        if response.status not in (200, 201):
            message = f"Error storing visit: {response.status}"
            if response_data.strip():
                message = f"{message}. Response: {response_data.strip()}"
            raise DataFailureException(url,
                                       response.status,
                                       message)
        return json.loads(response_data) if response_data.strip() else {}

    def get_current_quarter_visits(self, syskey):
        """
        Returns a list of visits for the given syskey in the current quarter.
        """
        url = f"{self.API}/visit/external_student/{syskey}"
        response = self.dao.getURL(url)
        if response.status != 200:
            raise DataFailureException(url,
                                       response.status,
                                       "Error getting visits for syskey "
                                       f"{syskey}: {response.status}")
        data = json.loads(response.data)
        visits = []
        for visit in data:
            checkout_raw = visit.get('checkout_date')
            visits.append(CompassVisitModel(
                student_netid=visit.get('student_netid') or '',
                visit_type=visit.get('visit_type') or '',
                course_code=visit.get('course_code') or '',
                tutoring_option=visit.get('tutoring_option') or '',
                checkin_date=parse_datetime(visit.get('checkin_date')),
                checkout_date=(
                    parse_datetime(checkout_raw) if checkout_raw else None
                ),
            ))
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
            "checkout_date": (
                self.checkout_date.isoformat() if self.checkout_date else None
            )
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
            "check_in_date": (
                self.checkin_date.isoformat() if self.checkin_date else None
            ),
            "check_out_date": (
                self.checkout_date.isoformat() if self.checkout_date else None
            ),
            "active_minutes": active_minutes,
        }
