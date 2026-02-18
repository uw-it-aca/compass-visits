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
        response = self.get_response('student_profile', netid='bthompson')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['current_state'], "none")
        self.assertIsNone(data['visit'])

    def test_not_verified_visit(self):
        response = self.get_response('student_profile', netid='asmith')
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
        self.assertEqual(data['student_name'], "James Average")
        self.assertIn('photo_url', data)
        self.assertEqual(data['photo_url'], "https://example.com/photo.jpg")
        self.assertIn('total_hours', data)
        self.assertEqual(data['total_hours'], 3.75)
