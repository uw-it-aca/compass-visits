# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re

from django.test import TestCase

from compass_visits.templatetags.vite import vite_scripts, vite_styles


class ViteTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_vite_styles(self):
        entries = ("compass_visits_vue/main.js",)
        link = vite_styles(*entries)
        pattern = re.compile(r'<link\s+[^>]*href="[^"]*main-[^"]*"[^>]*>')
        self.assertTrue(pattern.search(link))

    def test_vite_scripts(self):
        entries = ("compass_visits_vue/main.js",)
        script = vite_scripts(*entries)
        pattern = re.compile(
            r'<script\s+[^>]*src="[^"]*main-[^"]*"[^>]*></script>'
        )
        self.assertTrue(pattern.search(script))

    def test_duplicate(self):
        entries = ("compass_visits_vue/main.js", "compass_visits_vue/main.js")
        script = vite_scripts(*entries)
        pattern = re.compile(
            r'<script\s+[^>]*src="[^"]*main-[^"]*"[^>]*></script>'
        )
        self.assertTrue(pattern.search(script))
