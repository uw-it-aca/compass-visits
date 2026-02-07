# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APITestCase


class VisitOptionsAPITestCase(APITestCase):
    def test_get_visit_options(self):
        response = self.client.get('/api/v1/visitoptions/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('program_areas', data)
        self.assertIn('tutoring_options', data)
        self.assertIn('writing_services', data)
        self.assertIsInstance(data['program_areas'], list)
        self.assertIsInstance(data['tutoring_options'], list)
        self.assertIsInstance(data['writing_services'], list)

        self.assertEqual(len(data['program_areas']), 8)
        self.assertEqual(data['program_areas'][0]['name'],
                         'Biology/Natural Sci')
        self.assertEqual(data['program_areas'][0]['id'], 1)
        self.assertEqual(len(data['tutoring_options']), 2)
        self.assertEqual(data['tutoring_options'][0]['name'], 'Drop In')
        self.assertEqual(data['tutoring_options'][0]['id'], 1)
        self.assertEqual(len(data['writing_services']), 6)
        self.assertEqual(data['writing_services'][0]['name'], 'Application')
        self.assertEqual(data['writing_services'][0]['id'], 1)
