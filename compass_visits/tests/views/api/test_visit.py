# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APITestCase
from compass_visits.models import Visit


class VisitAPITestCase(APITestCase):
    def test_patch_visit_checked_out(self):
        response = self.patch_response('visit_detail',
                                       url_args={'visit_id': 1},
                                       netid='javerage',
                                       data={'checkout': True})

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['error'], "Visit is already checked out")

    def test_patch_visit_not_verified_checkout(self):
        response = self.patch_response('visit_detail',
                                       url_args={'visit_id': 2},
                                       netid='asmith',
                                       data={'checkout': True})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['error'], "Visit must be verified"
                                        " before checkout")

    def test_patch_visit_checkout_success(self):
        response = self.patch_response('visit_detail',
                                       url_args={'visit_id': 5},
                                       netid='dlee',
                                       data={'checkout': True})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data['check_out_date'])

    def test_delete_visit(self):
        response = self.delete_response('visit_detail',
                                        url_args={'visit_id': 6},
                                        netid='dlee')
        self.assertEqual(response.status_code, 200)
        # Verify visit is deleted
        with self.assertRaises(Visit.DoesNotExist):
            Visit.objects.get(id=6)

    def test_delete_visit_not_found(self):
        response = self.delete_response('visit_detail',
                                        url_args={'visit_id': 999},
                                        netid='dlee')
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data['error'], "Visit not found")

    def test_post_visit(self):
        new_visit_data = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        response = self.post_response('visit',
                                      netid='jnew',
                                      data=new_visit_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data['program_area'], 'Biology/Natural Sci')
        self.assertEqual(data['tutoring_option'], 'Drop In')
        self.assertEqual(data['writing_service'], 'Application')

    def test_already_active_visit(self):
        new_visit_data = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        response = self.post_response('visit',
                                      netid='javerage',
                                      data=new_visit_data)
        print(response.status_code, response.json())
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['error'],
                         "Student already has an active visit")
