# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.utils import timezone
from compass_visits.exceptions import ValidationError
from compass_visits.models import Visit
from compass_visits.tests import CompassVisitsTestCase
from compass_visits.dao.visit_dao import (get_active_visit_for_student,
                                          get_completed_visits_by_netid,
                                          get_visits_pending_checkout,
                                          get_visits_pending_verification,
                                          validate_visit_data,
                                          student_update_visit,
                                          create_visit_from_request,
                                          get_total_hours_by_netid,
                                          get_student_state,
                                          manager_create_visit_from_request,
                                          manager_update_visit)


class VisitDAOTest(CompassVisitsTestCase):
    def test_get_active_visit_for_student(self):
        netid = "asmith"
        visit = get_active_visit_for_student(netid)
        self.assertIsNotNone(visit)

        netid = "javerage"
        visit = get_active_visit_for_student(netid)
        self.assertEqual(visit.id, 12)

    def test_get_active_multuiple_visits_for_student(self):
        netid = "multivisituser"
        v1 = Visit.objects.create(
            student_netid=netid,
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=False
        )
        v2 = Visit.objects.create(
            student_netid=netid,
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=False,
            check_in_date=timezone.now() + timezone.timedelta(minutes=5)
        )
        visit = get_active_visit_for_student(netid)
        self.assertIsNotNone(visit)
        self.assertEqual(visit.id, v2.id)

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
            student_netid="bwayne",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True
        )
        request_data = {
            "checkout": True,
        }
        try:
            student_update_visit(visit, request_data)
        except Exception as e:
            self.fail(f"update_visit raised an exception unexpectedly: {e}")
        self.assertIsNotNone(visit.check_out_date)

    def test_update_unverified_visit(self):
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
            student_update_visit(unverified_visit, request_data)
        self.assertEqual(str(context.exception),
                         "Visit must be verified before checkout")

    def test_update_checked_out_visit(self):
        visit = Visit.objects.create(
            student_netid="bwayne",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=timezone.now()
        )
        request_data = {
            "checkout": True,
        }
        with self.assertRaises(ValidationError) as context:
            student_update_visit(visit, request_data)
        self.assertEqual(str(context.exception),
                         "Visit is already checked out")

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
            student_update_visit(unverified_visit, request_data)
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

    def test_get_student_state(self):
        active_visit = Visit.objects.create(
            student_netid="testuser",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True
        )
        self.assertEqual(get_student_state(active_visit), "active")

        pending_visit = Visit.objects.create(
            student_netid="testuser2",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=False
        )
        self.assertEqual(get_student_state(pending_visit),
                         "pending_verification")

        checked_out_visit = Visit.objects.create(
            student_netid="testuser3",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=timezone.now()
        )
        self.assertEqual(get_student_state(checked_out_visit), "none")

        self.assertEqual(get_student_state(None), "none")

    def test_get_visits_pending_verification(self):
        Visit.objects.all().delete()
        Visit.objects.create(
            student_netid="pendinguser",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=False
        )
        Visit.objects.create(
            student_netid="verifieduser",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True
        )
        pending_visits = get_visits_pending_verification()
        self.assertEqual(pending_visits.count(), 1)
        self.assertEqual(pending_visits.first().student_netid, "pendinguser")

    def test_get_visits_pending_checkout(self):
        Visit.objects.all().delete()
        Visit.objects.create(
            student_netid="pendingcheckoutuser",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=None
        )
        Visit.objects.create(
            student_netid="checkedoutuser",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=timezone.now()
        )
        pending_checkout_visits = get_visits_pending_checkout()
        self.assertEqual(pending_checkout_visits.count(), 1)
        self.assertEqual(pending_checkout_visits.first().student_netid,
                         "pendingcheckoutuser")

    def test_get_completed_visits_by_netid(self):
        Visit.objects.all().delete()
        Visit.objects.create(
            student_netid="completeduser",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=timezone.now()
        )
        Visit.objects.create(
            student_netid="inprogressuser",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=None
        )
        completed_visits = get_completed_visits_by_netid("completeduser")
        self.assertEqual(completed_visits.count(), 1)
        self.assertEqual(completed_visits.first().student_netid,
                         "completeduser")

    def test_manager_create_visit_from_request(self):
        request_data = {
            "student_netid": "newstudent",
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
            "course": None,
            "verify": True,
            "checkout": True
        }
        visit = manager_create_visit_from_request(request_data)
        self.assertEqual(visit.student_netid, request_data['student_netid'])
        self.assertEqual(visit.program_area.id, request_data['program_area'])
        self.assertEqual(visit.tutoring_option.id,
                         request_data['tutoring_option'])
        self.assertEqual(visit.writing_service.id,
                         request_data['writing_service'])
        self.assertIsNone(visit.course)
        self.assertTrue(visit.is_verified)
        self.assertIsNotNone(visit.check_out_date)

        request_data = {
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        with self.assertRaises(ValidationError) as context:
            manager_create_visit_from_request(request_data)
        self.assertIn("student_netid is required",
                      str(context.exception))

        request_data = {
            "student_netid": "newstudent2",
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
            "checkout": True
        }
        visit = manager_create_visit_from_request(request_data)
        self.assertTrue(visit.is_verified)

    def test_manager_update_visit(self):
        visit = Visit.objects.create(
            student_netid="updatetestuser",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
        )
        request_data = {
            "verify": True,
            "checkout": True
        }
        try:
            manager_update_visit(visit, request_data)
        except Exception as e:
            self.fail(f"manager_update_visit raised an exception "
                      f"unexpectedly: {e}")
        self.assertTrue(visit.is_verified)
        self.assertIsNotNone(visit.check_out_date)

    def test_manager_update_visit_invalid_checkout(self):
        visit = Visit.objects.create(
            student_netid="updatetestuser2",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
        )
        request_data = {
            "checkout": True
        }
        with self.assertRaises(ValidationError) as context:
            manager_update_visit(visit, request_data)
        self.assertEqual(str(context.exception),
                         "Visit must be verified before checkout")
        self.assertFalse(visit.is_verified)
        self.assertIsNone(visit.check_out_date)

    def test_manager_update_visit_already_checked_out(self):
        visit = Visit.objects.create(
            student_netid="updatetestuser3",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=timezone.now()
        )
        request_data = {
            "checkout": True
        }
        with self.assertRaises(ValidationError) as context:
            manager_update_visit(visit, request_data)
        self.assertEqual(str(context.exception),
                         "Visit is already checked out")

    def test_manager_update_visit_already_verified(self):
        visit = Visit.objects.create(
            student_netid="updatetestuser4",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True
        )
        request_data = {
            "verify": True
        }
        with self.assertRaises(ValidationError) as context:
            manager_update_visit(visit, request_data)
        self.assertEqual(str(context.exception),
                         "Visit is already verified")
