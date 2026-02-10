# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APITestCase


class StudentAPITestCase(APITestCase):
    def test_get_active_state(self):
        response = self.get_response('student_state', netid='javerage')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['state'], "active")
        self.assertEqual(data['visit']['id'], 12)

    def test_no_active_visit(self):
        response = self.get_response('student_state', netid='bthompson')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['state'], "none")
        self.assertNotIn('visit', data)

    def test_not_verified_visit(self):
        response = self.get_response('student_state', netid='asmith')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['state'], "pending_verification")
        self.assertEqual(data['visit']['id'], 2)

    def test_new_user(self):
        response = self.get_response('student_state', netid='newuser')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['state'], "none")
        self.assertNotIn('visit', data)
