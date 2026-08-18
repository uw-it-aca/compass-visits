# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone

from compass_visits.models import Visit
from compass_visits.tests import CompassVisitsTestCase


class TestSyncCompletedVisits(CompassVisitsTestCase):
    @patch("compass_visits.management.commands.sync_completed_visits.Compass")
    @patch(
        "compass_visits.management.commands."
        "sync_completed_visits.map_visit_to_compass_model"
    )
    def test_sync_success_deletes_visit(
        self,
        mock_map_visit,
        mock_compass_cls,
    ):
        Visit.objects.all().delete()
        visit = Visit.objects.create(
            student_syskey="000043900",
            student_netid="j043900",
            program_area="ic-drop-in-tutoring",
            tutoring_option="drop-in",
            course="CHEM 101",
            is_verified=True,
            check_out_date=timezone.now(),
        )

        mock_map_visit.return_value = {"visit": "payload"}
        mock_compass = mock_compass_cls.return_value
        mock_compass.store_visit.return_value = {"ok": True}

        call_command("sync_completed_visits")

        self.assertFalse(Visit.objects.filter(id=visit.id).exists())
        mock_map_visit.assert_called_once()
        self.assertEqual(mock_compass.store_visit.call_count, 1)

    @patch("compass_visits.management.commands.sync_completed_visits.Compass")
    @patch(
        "compass_visits.management.commands."
        "sync_completed_visits.map_visit_to_compass_model"
    )
    def test_sync_failure_keeps_visit_and_errors(self, mock_map_visit,
                                                 mock_compass_cls):
        Visit.objects.all().delete()
        visit = Visit.objects.create(
            student_syskey="000043901",
            student_netid="j043901",
            program_area="ic-drop-in-tutoring",
            tutoring_option="drop-in",
            writing_service_id=1,
            is_verified=True,
            check_out_date=timezone.now(),
        )

        mock_map_visit.return_value = {"visit": "payload"}
        mock_compass = mock_compass_cls.return_value
        mock_compass.store_visit.side_effect = Exception("boom")

        with self.assertRaises(CommandError):
            call_command("sync_completed_visits")

        self.assertTrue(Visit.objects.filter(id=visit.id).exists())

    @patch("compass_visits.management.commands.sync_completed_visits.Compass")
    @patch(
        "compass_visits.management.commands."
        "sync_completed_visits.map_visit_to_compass_model"
    )
    def test_limit_option(self, mock_map_visit, mock_compass_cls):
        Visit.objects.all().delete()
        Visit.objects.create(
            student_syskey="000043902",
            student_netid="j043902",
            program_area="ic-drop-in-tutoring",
            tutoring_option="drop-in",
            course="BIO 101",
            is_verified=True,
            check_out_date=timezone.now(),
        )
        Visit.objects.create(
            student_syskey="000043903",
            student_netid="j043903",
            program_area="ic-drop-in-tutoring",
            tutoring_option="drop-in",
            course="BIO 102",
            is_verified=True,
            check_out_date=timezone.now(),
        )

        mock_map_visit.return_value = {"visit": "payload"}
        mock_compass = mock_compass_cls.return_value
        mock_compass.store_visit.return_value = {"ok": True}

        call_command("sync_completed_visits", limit=1)

        self.assertEqual(Visit.objects.count(), 1)
        self.assertEqual(mock_compass.store_visit.call_count, 1)
