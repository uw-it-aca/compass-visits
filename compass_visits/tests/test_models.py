# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import CompassVisitsTestCase
from compass_visits.models import Visit
from django.utils import timezone


class VisitModelTest(CompassVisitsTestCase):

    def setUp(self):
        self.sample_visit = Visit.objects.create(
            student_syskey="012345678",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
        )
        return super().setUp()

    def test_json_data(self):
        json_data = self.sample_visit.json_data()
        self.assertEqual(json_data['id'], self.sample_visit.id)
        self.assertEqual(json_data['student_syskey'],
                         self.sample_visit.student_syskey)
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

    def test_active_duration(self):
        # Simulate an active visit by setting check_in_date to 30 minutes ago
        self.sample_visit.check_in_date =\
            self.sample_visit.check_in_date - timezone.timedelta(minutes=30)
        self.sample_visit.is_verified = True
        self.sample_visit.save()
        json_data = self.sample_visit.json_data()
        self.assertIn('active_minutes', json_data)
        self.assertEqual(json_data['active_minutes'], 30)
