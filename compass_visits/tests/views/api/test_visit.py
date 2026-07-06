# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APILoginTestCase
from compass_visits.models import Visit
from restclients_core.exceptions import DataFailureException
from unittest.mock import patch


class VisitAPITestCase(APILoginTestCase):
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
                                       netid='jnewstudent',
                                       data={'checkout': True})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['error'], "Visit must be verified"
                                        " before checkout")

    @patch('userservice.user.UserService.get_user')
    @patch('userservice.user.UserService.get_override_user')
    def test_patch_visit_checkout_success(self,
                                          mock_get_override_user,
                                          mock_get_user):
        mock_get_user.return_value = 'newuser'
        mock_get_override_user.return_value = None
        response = self.patch_response('visit_detail',
                                       url_args={'visit_id': 5},
                                       data={'checkout': True},
                                       netid='newuser')
        self.assertEqual(response.status_code, 403)

        with self.settings(ALLOW_USER_OVERRIDE_FOR_WRITE=False):
            mock_get_user.return_value = 'newuser'
            mock_get_override_user.return_value = 'javerage'
            response = self.patch_response('visit_detail',
                                           url_args={'visit_id': 5},
                                           data={'checkout': True},
                                           netid='newuser')
            self.assertEqual(response.status_code, 403)

        mock_get_user.return_value = 'jbothell'
        mock_get_override_user.return_value = None
        response = self.patch_response('visit_detail',
                                       url_args={'visit_id': 5},
                                       data={'checkout': True},
                                       netid='jbothell')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data['check_out_date'])

    @patch('userservice.user.UserService.get_user')
    @patch('userservice.user.UserService.get_override_user')
    def test_delete_visit(self, mock_get_override_user, mock_get_user):
        mock_get_user.return_value = 'javerage'
        response = self.delete_response('visit_detail',
                                        url_args={'visit_id': 6},
                                        netid='javerage')
        self.assertEqual(response.status_code, 403)

        with self.settings(ALLOW_USER_OVERRIDE_FOR_WRITE=False):
            mock_get_user.return_value = 'jbothell'
            mock_get_override_user.return_value = "javerage"
            response = self.delete_response('visit_detail',
                                            url_args={'visit_id': 6},
                                            netid='javerage')
            self.assertEqual(response.status_code, 403)

        mock_get_user.return_value = 'bill'
        mock_get_override_user.return_value = None
        response = self.delete_response('visit_detail',
                                        url_args={'visit_id': 6},
                                        netid='javerage')
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

    @patch('userservice.user.UserService.get_override_user')
    def test_post_visit(self, mock_get_override_user):
        mock_get_override_user.return_value = None
        new_visit_data = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        response = self.post_response('visit',
                                      netid='newuser',
                                      data=new_visit_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data['program_area'], 'Biology/Natural Sci')
        self.assertEqual(data['tutoring_option'], 'Drop In')
        self.assertEqual(data['writing_service'], 'Application')

        with self.settings(ALLOW_USER_OVERRIDE_FOR_WRITE=False):
            mock_get_override_user.return_value = 'javerage'
            response = self.post_response('visit',
                                          netid='jnew',
                                          data=new_visit_data)
            self.assertEqual(response.status_code, 403)

    def test_already_active_visit(self):
        new_visit_data = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        old_visit = Visit.objects.get(id=12)
        self.assertEqual(old_visit.check_out_date, None)
        response = self.post_response('visit',
                                      netid='javerage',
                                      data=new_visit_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        old_visit.refresh_from_db()
        self.assertIsNotNone(old_visit.check_out_date)
        self.assertEqual(data['program_area'], 'Biology/Natural Sci')
        self.assertEqual(data['tutoring_option'], 'Drop In')
        self.assertEqual(data['writing_service'], 'Application')
        new_visit = Visit.objects.get(id=data['id'])
        self.assertEqual(new_visit.is_verified, True)
        self.assertEqual(new_visit.check_out_date, None)

    def test_post_visit_course_too_long(self):
        response = self.post_response('visit',
                                      netid='newuser',
                                      data={
                                          "program_area": 1,
                                          "tutoring_option": 1,
                                          "course": "A" * 256,
                                      })
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'],
                         "course exceeds max length of 255")

    @patch('compass_visits.views.api.visit_student.get_syskey_by_netid')
    @patch('userservice.user.UserService.get_override_user')
    def test_post_visit_data_failure(self,
                                     mock_get_override_user,
                                     mock_get_syskey):
        mock_get_override_user.return_value = None
        mock_get_syskey.side_effect = DataFailureException(
            '/api/v1/person/newuser/full.json', 500, 'PWS error')
        response = self.post_response('visit',
                                      netid='newuser',
                                      data={"program_area": 1})
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'],
                         "Unable to retrieve student information")
