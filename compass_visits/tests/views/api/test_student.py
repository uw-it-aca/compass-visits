# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APILoginTestCase
from unittest.mock import patch
from restclients_core.exceptions import DataFailureException


class StudentAPITestCase(APILoginTestCase):
    def test_get_active_current_state(self):
        response = self.get_response('student_profile', netid='javerage')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['current_state'], "active")
        self.assertEqual(data['visit']['id'], 12)

    def test_no_active_visit(self):
        response = self.get_response('student_profile', netid='jinternational')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertNotIn('current_state', data)
        self.assertNotIn('visit', data)

    def test_not_verified_visit(self):
        response = self.get_response('student_profile', netid='jnewstudent')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['current_state'], "pending_verification")
        self.assertEqual(data['visit']['id'], 2)

    def test_new_user(self):
        response = self.get_response('student_profile', netid='newuser')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['current_state'], "none")
        self.assertIsNone(data['visit'])

    def test_profile_params(self):
        response = self.get_response('student_profile', netid='javerage')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('netid', data)
        self.assertEqual(data['netid'], 'javerage')
        self.assertIn('student_name', data)
        self.assertEqual(data['student_name'], "Jamesy McJamesy")
        self.assertIn('photo', data)
        self.assertTrue(data['photo'].startswith("/9j/4AAQSkZJRgABAQAAAQ"))
        self.assertIn('total_minutes', data)
        self.assertEqual(data['total_minutes'], 225.0)

    def test_get_student_visits(self):
        response = self.get_response('student_visits', netid='javerage')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3)
        self.assertIn('student_netid', data[0])
        self.assertIn('check_in_date', data[0])
        self.assertIn('check_out_date', data[0])
        self.assertIn('course', data[0])
        self.assertIn('active_minutes', data[0])
        self.assertEqual(data[0]['student_netid'], 'javerage')
        self.assertGreaterEqual(data[0]['check_in_date'],
                                data[1]['check_in_date'])
        self.assertGreaterEqual(data[1]['check_in_date'],
                                data[2]['check_in_date'])

    def test_get_student_visits_no_visits(self):
        response = self.get_response('student_visits', netid='newuser')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)

    @patch('compass_visits.views.api.visit_student'
           '.get_current_quarter_visits_by_syskey')
    def test_get_student_visits_compass_error(self, mock_get_visits):
        mock_get_visits.side_effect = DataFailureException(
            '/api/v1/visit/external_student/000083856', 500, 'Compass error')
        response = self.get_response('student_visits', netid='javerage')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'],
                         "Unable to retrieve student information")

    def test_not_ic_eligible(self):
        response = self.get_response('student_profile', netid='jinternational')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['ic_elligible'])

    def test_no_compass_response(self):
        response = self.get_response('student_profile', netid='jerror')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'],
                         "Unable to retrieve student information")
