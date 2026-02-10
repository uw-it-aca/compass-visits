# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import CompassVisitsTestCase
from compass_visits.dao.visit import (get_active_visit_for_student,
                                      validate_visit_data)


class VisitDAOTest(CompassVisitsTestCase):
    def test_get_active_visit_for_student(self):
        netid = "asmith"
        visit = get_active_visit_for_student(netid)
        self.assertIsNotNone(visit)

        netid = "javerage"
        visit = get_active_visit_for_student(netid)
        self.assertIsNone(visit)

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
