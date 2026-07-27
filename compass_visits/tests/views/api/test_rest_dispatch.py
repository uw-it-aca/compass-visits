# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase

from compass_visits.views.api import RESTDispatch


class RESTDispatchTestCase(TestCase):
    def test_json_response(self):
        content = {"message": "Hello, world!"}
        response = RESTDispatch.json_response(content=content, status=200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(response.content, content)

    def test_bad_json_response(self):
        # Test that a TypeError in json.dumps results in a 400 response
        content = {"message": set([1, 2, 3])}  # sets are not JSON serializable
        response = RESTDispatch.json_response(content=content, status=200)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_error_response(self):
        message = "An error occurred"
        content = {"details": "Something went wrong"}
        response = RESTDispatch.error_response(status=400,
                                               message=message,
                                               content=content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        expected_content = {"error": message,
                            "details": "Something went wrong"}
        self.assertJSONEqual(response.content, expected_content)
