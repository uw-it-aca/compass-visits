# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APITestCase


class VisitExternalAPITestCase(APITestCase):

    def test_get_visit_admin_list(self):
        response = self.get_response('visit_admin_list')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('pending_verification', data)
        self.assertEqual(len(data['pending_verification']), 7)
        self.assertEqual(data['pending_verification'][0]['id'], 2)
        self.assertIn('pending_checkout', data)
        self.assertEqual(len(data['pending_checkout']), 2)
        self.assertEqual(data['pending_checkout'][0]['id'], 5)

    def test_get_compass_student_visits(self):
        response = self.get_response('compass_student_visits',
                                     url_args={'student_netid': 'javerage'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], 11)
        self.assertEqual(data[1]['id'], 1)
