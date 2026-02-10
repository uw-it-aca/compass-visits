# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from compass_visits.models import (ProgramArea,
                                   TutoringOption,
                                   WritingService,
                                   Visit)
from django.core.management import call_command


class TestInitDb(TestCase):

    def test_init_db(self):
        self.assertEqual(ProgramArea.objects.count(), 0)
        self.assertEqual(TutoringOption.objects.count(), 0)
        self.assertEqual(WritingService.objects.count(), 0)
        self.assertEqual(Visit.objects.count(), 0)
        call_command('initialize_db')
        self.assertEqual(ProgramArea.objects.count(), 9)
        self.assertEqual(TutoringOption.objects.count(), 3)
        self.assertEqual(WritingService.objects.count(), 7)
        self.assertEqual(Visit.objects.count(), 12)
