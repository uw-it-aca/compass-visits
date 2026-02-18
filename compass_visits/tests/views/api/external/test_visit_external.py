# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APITokenTestCase
from compass_visits.models import Visit


class VisitExternalAPITestCase(APITokenTestCase):
    def test_bad_token(self):
        response = self.get_response('visit_admin_list',
                                     token='Token badtoken')
        self.assertEqual(response.status_code, 403)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid API token')

    def test_no_token(self):
        response = self.get_response('visit_admin_list', token=None)
        self.assertEqual(response.status_code, 403)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'API token is required')

    def test_bad_token_format(self):
        response = self.get_response('visit_admin_list',
                                     token='badformat')
        self.assertEqual(response.status_code, 403)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid API token format')

    def test_get_visit_admin_list(self):
        response = self.get_response('visit_admin_list',
                                     token='Token testtoken')
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
                                     url_args={'student_netid': 'javerage'},
                                     token='Token testtoken'
                                     )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], 11)
        self.assertEqual(data[1]['id'], 1)

    def test_manage_visits_patch(self):
        response = self.patch_response('manage_visit',
                                       url_args={'visit_id': 2},
                                       token='Token testtoken',
                                       data={'verify': True}
                                       )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], 2)
        self.assertTrue(data['is_verified'])

    def test_manage_visits_patch_visit_not_found(self):
        response = self.patch_response('manage_visit',
                                       url_args={'visit_id': 999},
                                       token='Token testtoken',
                                       data={'verify': True}
                                       )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Visit not found')

    def test_manage_visits_patch_validation_error(self):
        response = self.patch_response('manage_visit',
                                       url_args={'visit_id': 1},
                                       token='Token testtoken',
                                       data={'verify': True}
                                       )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Visit is already verified')

        response = self.patch_response('manage_visit',
                                       url_args={'visit_id': 1},
                                       token='Token testtoken',
                                       data={'checkout': True}
                                       )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Visit is already checked out')

        response = self.patch_response('manage_visit',
                                       url_args={'visit_id': 2},
                                       token='Token testtoken',
                                       data={'checkout': True}
                                       )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Visit must be verified before'
                                        ' checkout')

    def test_manage_visits_post(self):
        new_visit_data = {
            'student_netid': 'newstudent',
            'program_area': 1,
            'tutoring_option': 1,
            'writing_service': 1,
            'check_in_date': '2024-01-01T10:00:00Z',
            'verify': True
        }
        response = self.post_response('manage_visits',
                                      token='Token testtoken',
                                      data=new_visit_data
                                      )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['student_netid'], 'newstudent')
        self.assertEqual(data['program_area'], 'Biology/Natural Sci')
        self.assertEqual(data['tutoring_option'], 'Drop In')
        self.assertEqual(data['writing_service'], 'Application')

        self.assertIsNotNone(data['check_in_date'])
        self.assertIsNone(data['check_out_date'])
        self.assertTrue(data['is_verified'])

    def test_manage_visits_post_validation_error(self):
        new_visit_data = {
            'program_area': 1,
            'tutoring_option': 1,
            'writing_service': 1,
            'check_in_date': '2024-01-01T10:00:00Z',
            'verify': True
        }
        response = self.post_response('manage_visits',
                                      token='Token testtoken',
                                      data=new_visit_data
                                      )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'student_netid is required')

    def test_manage_visits_delete(self):
        response = self.delete_response('manage_visit',
                                        url_args={'visit_id': 3},
                                        token='Token testtoken'
                                        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {})
        with self.assertRaises(Visit.DoesNotExist):
            Visit.objects.get(id=3)
