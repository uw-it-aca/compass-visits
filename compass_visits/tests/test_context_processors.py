# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase

from compass_visits.context_processors import django_debug, google_analytics


class ContextProcessorsTestCase(TestCase):
    def test_google_analytics(self):
        with self.settings(GOOGLE_ANALYTICS_KEY='UA-12345678-1'):
            context = google_analytics(None)
            self.assertIn('google_analytics', context)
            self.assertEqual(context['google_analytics'], 'UA-12345678-1')

    def test_django_debug(self):
        with self.settings(DEBUG=True):
            context = django_debug(None)
            self.assertIn('django_debug', context)
            self.assertTrue(context['django_debug'])

        with self.settings(DEBUG=False):
            context = django_debug(None)
            self.assertIn('django_debug', context)
            self.assertFalse(context['django_debug'])
