# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime
from unittest.mock import patch

from django.utils import timezone

from compass_visits.dao.compass import CompassVisitModel
from compass_visits.dao.visit_dao import (
    checkout_active_verified_visit,
    create_visit_from_request,
    get_active_visit_for_student,
    get_completed_visits_by_syskey,
    get_current_quarter_visits_by_syskey,
    get_student_state,
    get_total_minutes_by_syskey,
    get_visits_pending_checkout,
    get_visits_pending_verification,
    manager_create_visit_from_request,
    manager_update_visit,
    student_update_visit,
    validate_visit_data,
)
from compass_visits.exceptions import ValidationError
from compass_visits.models import Visit
from compass_visits.tests import CompassVisitsTestCase


class VisitDAOTest(CompassVisitsTestCase):
    def test_get_active_visit_for_student(self):
        student_syskey = "000083857"
        visit = get_active_visit_for_student(student_syskey)
        self.assertIsNotNone(visit)

        student_syskey = "000083856"
        visit = get_active_visit_for_student(student_syskey)
        self.assertEqual(visit.id, 12)

    def test_get_active_multiple_visits_for_student(self):
        student_syskey = "000083851"
        Visit.objects.create(
            student_syskey=student_syskey,
            student_netid="j043851",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=False
        )
        v2 = Visit.objects.create(
            student_syskey=student_syskey,
            student_netid="j043851",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=False,
            check_in_date=timezone.now() + timezone.timedelta(minutes=5)
        )
        visit = get_active_visit_for_student(student_syskey)
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
        except Exception:
            self.fail("validate_visit_data raised an "
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

        long_course = {
            "program_area": 1,
            "tutoring_option": 1,
            "course": "A" * 256,
        }
        with self.assertRaises(Exception) as context:
            validate_visit_data(long_course)
        self.assertIn("course exceeds max length of 255",
                      str(context.exception))

    def test_update_visit(self):
        visit = Visit.objects.create(
            student_syskey="000043856",
            student_netid="j043856",
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
            student_syskey="000043856",
            student_netid="j043856",
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
            student_syskey="000043856",
            student_netid="j043856",
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
            student_syskey="000043856",
            student_netid="j043856",
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
        student_syskey = "000043856"
        student_netid = "j043856"
        visit = create_visit_from_request(request_data,
                                          student_syskey,
                                          student_netid)
        self.assertEqual(visit.student_syskey, student_syskey)
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
        student_syskey = "000043857"
        student_netid = "j043857"
        visit = create_visit_from_request(request_data,
                                          student_syskey,
                                          student_netid)
        self.assertEqual(visit.course, request_data['course'])
        self.assertIsNone(visit.writing_service)
        visit.delete()

        visit = create_visit_from_request(request_data,
                                          student_syskey,
                                          student_netid,
                                          verified=True)
        self.assertTrue(visit.is_verified)

        request_data = {
            "program_area": 1,
            "tutoring_option": 1,
            "course": "A" * 256,
        }
        with self.assertRaises(ValidationError) as context:
            create_visit_from_request(request_data,
                                      "000049999",
                                      "j049999")
        self.assertEqual(str(context.exception),
                         "course exceeds max length of 255")

    def test_create_from_request_with_active_visit(self):
        Visit.objects.all().delete()  # Clear existing visits

        student_syskey = "000043858"
        Visit.objects.create(
            student_syskey=student_syskey,
            student_netid="j043858",
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
            create_visit_from_request(request_data,
                                      student_syskey,
                                      "j043858")
        self.assertEqual(str(context.exception),
                         "Student already has an active visit")

    def test_get_total_minutes_by_syskey(self):
        # multi with in progress
        total_minutes = get_total_minutes_by_syskey("000083856")
        self.assertEqual(total_minutes, 225)

        # single visit
        total_minutes = get_total_minutes_by_syskey("000083859")
        self.assertEqual(total_minutes, 60)

        # Only in progress
        total_minutes = get_total_minutes_by_syskey("000083857")
        self.assertEqual(total_minutes, 0)

        # No visits
        total_minutes = get_total_minutes_by_syskey("000000000")
        self.assertEqual(total_minutes, 0)

    def test_get_student_state(self):
        active_visit = Visit.objects.create(
            student_syskey="000043859",
            student_netid="j043859",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True
        )
        self.assertEqual(get_student_state(active_visit), "active")

        pending_visit = Visit.objects.create(
            student_syskey="000043860",
            student_netid="j043860",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=False
        )
        self.assertEqual(get_student_state(pending_visit),
                         "pending_verification")

        checked_out_visit = Visit.objects.create(
            student_syskey="000043861",
            student_netid="j043861",
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
            student_syskey="000043862",
            student_netid="j043862",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=False
        )
        Visit.objects.create(
            student_syskey="000043863",
            student_netid="j043863",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True
        )
        pending_visits = get_visits_pending_verification()
        self.assertEqual(pending_visits.count(), 1)
        self.assertEqual(pending_visits.first().student_syskey, "000043862")

    def test_get_visits_pending_checkout(self):
        Visit.objects.all().delete()
        Visit.objects.create(
            student_syskey="000043864",
            student_netid="j043864",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=None
        )
        Visit.objects.create(
            student_syskey="000043865",
            student_netid="j043865",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=timezone.now()
        )
        pending_checkout_visits = get_visits_pending_checkout()
        self.assertEqual(pending_checkout_visits.count(), 1)
        self.assertEqual(pending_checkout_visits.first().student_syskey,
                         "000043864")

    def test_get_completed_visits_by_syskey(self):
        Visit.objects.all().delete()
        Visit.objects.create(
            student_syskey="000043866",
            student_netid="j043866",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=timezone.now()
        )
        Visit.objects.create(
            student_syskey="000043867",
            student_netid="j043867",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=None
        )
        completed_visits = get_completed_visits_by_syskey("000043866")
        self.assertEqual(completed_visits.count(), 1)
        self.assertEqual(completed_visits.first().student_syskey,
                         "000043866")

    def test_manager_create_visit_from_request(self):
        request_data = {
            "student_syskey": "000043868",
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
            "course": None,
            "verify": True,
            "checkout": True
        }
        with patch(
            "compass_visits.dao.visit_dao.get_netid_by_syskey"
        ) as mock_get_netid:
            mock_get_netid.return_value = "j043868"
            visit = manager_create_visit_from_request(request_data)
        self.assertEqual(visit.student_syskey, request_data['student_syskey'])
        self.assertEqual(visit.student_netid, "j043868")
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
        self.assertIn("student_syskey is required",
                      str(context.exception))

        request_data = {
            "student_syskey": "000043869",
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 1,
            "checkout": True
        }
        with patch(
            "compass_visits.dao.visit_dao.get_netid_by_syskey"
        ) as mock_get_netid:
            mock_get_netid.return_value = "j043869"
            visit = manager_create_visit_from_request(request_data)
        self.assertTrue(visit.is_verified)

        request_data = {
            "student_syskey": "000043870",
            "program_area": 99,
            "tutoring_option": 1,
            "writing_service": 1,
        }
        with patch(
            "compass_visits.dao.visit_dao.get_netid_by_syskey"
        ) as mock_get_netid:
            mock_get_netid.return_value = "j043870"
            with self.assertRaises(ValidationError) as context:
                manager_create_visit_from_request(request_data)
        self.assertIn("Invalid program_area", str(context.exception))

        request_data = {
            "student_syskey": "000043870",
            "program_area": 1,
            "tutoring_option": 99,
            "writing_service": 1,
        }
        with patch(
            "compass_visits.dao.visit_dao.get_netid_by_syskey"
        ) as mock_get_netid:
            mock_get_netid.return_value = "j043870"
            with self.assertRaises(ValidationError) as context:
                manager_create_visit_from_request(request_data)
        self.assertIn("Invalid tutoring_option", str(context.exception))

        request_data = {
            "student_syskey": "000043870",
            "program_area": 1,
            "tutoring_option": 1,
            "writing_service": 99,
        }
        with patch(
            "compass_visits.dao.visit_dao.get_netid_by_syskey"
        ) as mock_get_netid:
            mock_get_netid.return_value = "j043870"
            with self.assertRaises(ValidationError) as context:
                manager_create_visit_from_request(request_data)
        self.assertIn("Invalid writing_service", str(context.exception))

        request_data = {
            "student_syskey": "000043871",
            "program_area": 1,
            "tutoring_option": 1,
            "course": "A" * 256,
        }
        with patch(
            "compass_visits.dao.visit_dao.get_netid_by_syskey"
        ) as mock_get_netid:
            mock_get_netid.return_value = "j043871"
            with self.assertRaises(ValidationError) as context:
                manager_create_visit_from_request(request_data)
        self.assertEqual(str(context.exception),
                         "course exceeds max length of 255")

    def test_manager_update_visit(self):
        visit = Visit.objects.create(
            student_syskey="000043870",
            student_netid="j043870",
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
            student_syskey="000043871",
            student_netid="j043871",
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
            student_syskey="000043872",
            student_netid="j043872",
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
            student_syskey="000043873",
            student_netid="j043873",
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

    def test_checkout_active_verified_visit(self):
        student_syskey = "000043874"
        active_visit = Visit.objects.create(
            student_syskey=student_syskey,
            student_netid="j043874",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True
        )
        checkout_active_verified_visit(student_syskey)
        active_visit.refresh_from_db()
        self.assertIsNotNone(active_visit.check_out_date)

        # Test with no active verified visit
        student_syskey_no_active = "000043875"
        try:
            checkout_active_verified_visit(student_syskey_no_active)
        except Exception as e:
            self.fail(f"checkout_active_verified_visit raised an exception "
                      f"unexpectedly: {e}")

    @patch('compass_visits.dao.visit_dao.Compass.get_current_quarter_visits')
    def test_get_current_quarter_visits_by_syskey(self, mock_get_visits):
        visit_early = CompassVisitModel(
            student_netid="javerage",
            visit_type="Drop In",
            course_code="MATH 101",
            tutoring_option="Individual",
            checkin_date=datetime.datetime(2024, 8, 1, 10, 0,
                                           tzinfo=datetime.timezone.utc),
            checkout_date=datetime.datetime(2024, 8, 1, 10, 30,
                                            tzinfo=datetime.timezone.utc),
        )
        visit_late = CompassVisitModel(
            student_netid="javerage",
            visit_type="Drop In",
            course_code="CHEM 101",
            tutoring_option="Group",
            checkin_date=datetime.datetime(2024, 8, 1, 12, 0,
                                           tzinfo=datetime.timezone.utc),
            checkout_date=datetime.datetime(2024, 8, 1, 12, 45,
                                            tzinfo=datetime.timezone.utc),
        )
        mock_get_visits.return_value = [visit_early, visit_late]

        visits = get_current_quarter_visits_by_syskey("000083856")

        mock_get_visits.assert_called_once_with("000083856")
        self.assertEqual([v.course_code for v in visits],
                         ["CHEM 101", "MATH 101"])
        self.assertIn("checkin_date", visits[0].json_data())
