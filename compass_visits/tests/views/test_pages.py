# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime

from persistent_message.models import Message

from compass_visits.tests import APILoginTestCase


class PageViewTestCase(APILoginTestCase):

    def test_get_context_data(self):
        response = self.get_response('default_page', netid='javerage')
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertIn('user_netid', context)
        self.assertEqual(context['user_netid'], 'javerage')
        self.assertIn('user_override', context)
        self.assertEqual(context['user_override'], 'javerage')

    def test_message_context(self):
        Message.objects.create(
            content="This is a test message.",
            created=datetime.datetime.now(),
            level=Message.SUCCESS_LEVEL
        )
        response = self.get_response('default_page', netid='javerage')
        context = response.context
        self.assertIn('messages', context)
        self.assertEqual(len(context['messages']), 1)
        self.assertIn("This is a test message.", context['messages'][0])
        self.assertIn('message_level', context)
        self.assertEqual(context['message_level'], 'success')
