# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.exceptions import ValidationError
from compass_visits.models import Visit
from compass_visits.tests import CompassVisitsTestCase
from compass_visits.dao.visit import (get_active_visit_for_student,
                                      validate_visit_data, update_visit,
                                      create_visit_from_request,
                                      get_total_hours_by_netid)


class VisitDAOTest(CompassVisitsTestCase):
    def test_get_active_visit_for_student(self):
        netid = "asmith"
        visit = get_active_visit_for_student(netid)
        self.assertIsNotNone(visit)

        netid = "javerage"
        visit = get_active_visit_for_student(netid)
        self.assertEqual(visit.id, 12)

    def test_validate_visit_data(self):
        valid_request = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        try:
            validate_visit_data(valid_request)
        except Exception as e:
            self.fail(f"validate_visit_data raised an "
                      "exception unexpectedly: {e}")

        missing_program_area = {
            "tutoring_option": 1,
            "writing_service": 1,
        }
        with self.assertRaises(Exception) as context:
            validate_visit_data(missing_program_area)
        self.assertIn("program_area is required", str(context.exception))

        missing_tutoring_option = {
            "program_area": 1,
            "writing_service": 1,
        }
        with self.assertRaises(Exception) as context:
            validate_visit_data(missing_tutoring_option)
        self.assertIn("tutoring_option is required", str(context.exception))

        missing_writing_service_and_course = {
            "program_area": 1,
            "tutoring_option": 1,
        }
        with self.assertRaises(Exception) as context:
            validate_visit_data(missing_writing_service_and_course)
        self.assertIn("Either writing_service or course is required",
                      str(context.exception))

        both_writing_service_and_course = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
            "course": "ENGL101"
        }
        with self.assertRaises(Exception) as context:
            validate_visit_data(both_writing_service_and_course)
        self.assertIn("Only one of writing_service or course can be provided",
                      str(context.exception))

        invalid_program_area = {
            "program_area": 999,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        with self.assertRaises(Exception) as context:
            validate_visit_data(invalid_program_area)
        self.assertIn("Invalid program_area", str(context.exception))

        invalid_tutoring_option = {
            "program_area": 1,
            "tutoring_option": 999,
            "writing_service": 1,
        }
        with self.assertRaises(Exception) as context:
            validate_visit_data(invalid_tutoring_option)
        self.assertIn("Invalid tutoring_option", str(context.exception))

        invalid_writing_service = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 999,
        }
        with self.assertRaises(Exception) as context:
            validate_visit_data(invalid_writing_service)
        self.assertIn("Invalid writing_service", str(context.exception))

    def test_update_visit(self):
        visit = Visit.objects.create(
            student_netid="asmith",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
        )

        request_data = {
            "verify": True,
        }
        update_visit(visit, request_data)
        self.assertTrue(visit.is_verified)

        request_data = {
            "checkout": True,
        }
        update_visit(visit, request_data)
        self.assertIsNotNone(visit.check_out_date)

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
            update_visit(unverified_visit, request_data)
        self.assertEqual(str(context.exception),
                         "Visit must be verified before checkout")
        self.assertIsNone(unverified_visit.check_out_date)

    def test_create_from_request(self):
        request_data = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        student_netid = "jdoe"
        visit = create_visit_from_request(request_data, student_netid)
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
        student_netid = "janeaverage"
        visit = create_visit_from_request(request_data, student_netid)
        self.assertEqual(visit.course, request_data['course'])
        self.assertIsNone(visit.writing_service)

    def test_create_from_request_with_active_visit(self):
        Visit.objects.all().delete()  # Clear existing visits

        student_netid = "asmith"
        Visit.objects.create(
            student_netid=student_netid,
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
        )

        request_data = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        with self.assertRaises(ValidationError) as context:
            create_visit_from_request(request_data, student_netid)
        self.assertEqual(str(context.exception),
                         "Student already has an active visit")

    def test_get_total_hours_by_netid(self):
        # multi with in progress
        total_hours = get_total_hours_by_netid("javerage")
        self.assertEqual(total_hours, 3.75)

        # single visit
        total_hours = get_total_hours_by_netid("bthompson")
        self.assertEqual(total_hours, 1)

        # Only in progress
        total_hours = get_total_hours_by_netid("kmiller")
        self.assertEqual(total_hours, 0)

        # No visits
        total_hours = get_total_hours_by_netid("nobody")
        self.assertEqual(total_hours, 0)
