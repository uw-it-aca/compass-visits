# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import CompassVisitsTestCase
from compass_visits.models import Visit
from compass_visits.exceptions import ValidationError


class VisitModelTest(CompassVisitsTestCase):

    def setUp(self):
        self.sample_visit = Visit.objects.create(
            student_netid="asmith",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
        )
        return super().setUp()

    def test_create_from_request(self):
        request_data = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        student_netid = "javerage"
        visit = Visit.create_from_request(request_data, student_netid)
        self.assertEqual(visit.student_netid, student_netid)
        self.assertEqual(visit.program_area.id, request_data['program_area'])
        self.assertEqual(visit.tutoring_option.id,
                         request_data['tutoring_option'])
        self.assertEqual(visit.writing_service.id,
                         request_data['writing_service'])
        self.assertIsNone(visit.course)

        request_data = {
            "program_area": 1,
            "tutoring_option": 1,
            "course": "TRAIN 101",
        }
        visit = Visit.create_from_request(request_data, student_netid)
        self.assertEqual(visit.course, request_data['course'])
        self.assertIsNone(visit.writing_service)

    def test_json_data(self):
        json_data = self.sample_visit.json_data()
        self.assertEqual(json_data['id'], self.sample_visit.id)
        self.assertEqual(json_data['student_netid'],
                         self.sample_visit.student_netid)
        self.assertEqual(json_data['program_area'],
                         self.sample_visit.program_area.name)
        self.assertEqual(json_data['tutoring_option'],
                         self.sample_visit.tutoring_option.name)
        self.assertEqual(json_data['writing_service'],
                         self.sample_visit.writing_service.name)
        self.assertIsNone(json_data['course'])
        self.assertFalse(json_data['is_verified'])
        self.assertIsNotNone(json_data['check_in_date'])
        self.assertIsNone(json_data['check_out_date'])

    def test_update_visit(self):
        request_data = {
            "verify": True,
        }
        self.sample_visit.update_visit(request_data)
        self.assertTrue(self.sample_visit.is_verified)

        request_data = {
            "checkout": True,
        }
        self.sample_visit.update_visit(request_data)
        self.assertIsNotNone(self.sample_visit.check_out_date)

    def test_bad_update_visit(self):
        unverified_visit = Visit.objects.create(
            student_netid="bwayne",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
        )
        request_data = {
            "checkout": True,
        }
        with self.assertRaises(ValidationError) as context:
            unverified_visit.update_visit(request_data)
        self.assertEqual(str(context.exception),
                         "Visit must be verified before checkout")
        self.assertIsNone(unverified_visit.check_out_date)
