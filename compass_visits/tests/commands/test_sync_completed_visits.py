# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone

from compass_visits.models import Visit
from compass_visits.tests import CompassVisitsTestCase
from unittest.mock import patch


class TestSyncCompletedVisits(CompassVisitsTestCase):
    @patch("compass_visits.management.commands.sync_completed_visits.Compass")
    @patch("compass_visits.management.commands.sync_completed_visits.get_netid_by_syskey")
    def test_sync_success_deletes_visit(self, mock_get_netid, mock_compass_cls):
        Visit.objects.all().delete()
        visit = Visit.objects.create(
            student_syskey="000043900",
            student_netid="j043900",
            program_area_id=1,
            tutoring_option_id=1,
            course="CHEM 101",
            is_verified=True,
            check_out_date=timezone.now(),
        )

        mock_get_netid.return_value = "javerage"
        mock_compass = mock_compass_cls.return_value
        mock_compass.store_visit.return_value = {"ok": True}

        call_command("sync_completed_visits")

        self.assertFalse(Visit.objects.filter(id=visit.id).exists())
        mock_get_netid.assert_called_once_with("000043900")
        self.assertEqual(mock_compass.store_visit.call_count, 1)

    @patch("compass_visits.management.commands.sync_completed_visits.Compass")
    @patch("compass_visits.management.commands.sync_completed_visits.get_netid_by_syskey")
    def test_sync_failure_keeps_visit_and_errors(self, mock_get_netid,
                                                 mock_compass_cls):
        Visit.objects.all().delete()
        visit = Visit.objects.create(
            student_syskey="000043901",
            student_netid="j043901",
            program_area_id=1,
            tutoring_option_id=1,
            writing_service_id=1,
            is_verified=True,
            check_out_date=timezone.now(),
        )

        mock_get_netid.return_value = "javerage"
        mock_compass = mock_compass_cls.return_value
        mock_compass.store_visit.side_effect = Exception("boom")

        with self.assertRaises(CommandError):
            call_command("sync_completed_visits")

        self.assertTrue(Visit.objects.filter(id=visit.id).exists())

    @patch("compass_visits.management.commands.sync_completed_visits.Compass")
    @patch("compass_visits.management.commands.sync_completed_visits.get_netid_by_syskey")
    def test_limit_option(self, mock_get_netid, mock_compass_cls):
        Visit.objects.all().delete()
        Visit.objects.create(
            student_syskey="000043902",
            student_netid="j043902",
            program_area_id=1,
            tutoring_option_id=1,
            course="BIO 101",
            is_verified=True,
            check_out_date=timezone.now(),
        )
        Visit.objects.create(
            student_syskey="000043903",
            student_netid="j043903",
            program_area_id=1,
            tutoring_option_id=1,
            course="BIO 102",
            is_verified=True,
            check_out_date=timezone.now(),
        )

        mock_get_netid.return_value = "javerage"
        mock_compass = mock_compass_cls.return_value
        mock_compass.store_visit.return_value = {"ok": True}

        call_command("sync_completed_visits", limit=1)

        self.assertEqual(Visit.objects.count(), 1)
        self.assertEqual(mock_compass.store_visit.call_count, 1)
