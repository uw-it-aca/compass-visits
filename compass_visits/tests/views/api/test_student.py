# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APILoginTestCase


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
        self.assertEqual(data['current_state'], "none")
        self.assertIsNone(data['visit'])

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
        self.assertEqual(data[0]['id'], 11)
        self.assertEqual(data[1]['id'], 12)

    def test_get_student_visits_no_visits(self):
        response = self.get_response('student_visits', netid='newuser')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)
