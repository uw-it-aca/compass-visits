# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APILoginTestCase
from compass_visits.views.pages import PageView


class PageViewTestCase(APILoginTestCase):

    def test_get_context_data(self):
        response = self.get_response('default_page', netid='javerage')
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertIn('user_netid', context)
        self.assertEqual(context['user_netid'], 'javerage')
        self.assertIn('user_override', context)
        self.assertEqual(context['user_override'], 'javerage')
