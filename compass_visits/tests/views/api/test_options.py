# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APILoginTestCase


class VisitOptionsAPITestCase(APILoginTestCase):
    def test_get_visit_options(self):
        response = self.get_response('visit_options', netid='javerage')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('program_areas', data)
        self.assertIn('tutoring_options', data)
        self.assertIn('writing_services', data)
        self.assertIn('courses', data)
        self.assertIsInstance(data['program_areas'], list)
        self.assertIsInstance(data['tutoring_options'], list)
        self.assertIsInstance(data['writing_services'], list)

        self.assertEqual(len(data['program_areas']), 3)
        self.assertEqual(data['program_areas'][0]['name'],
                 'IC Drop-In Tutoring')
        self.assertEqual(data['program_areas'][0]['id'], 1)
        self.assertEqual(len(data['tutoring_options']), 3)
        self.assertEqual(data['tutoring_options'][0]['name'], 'Drop In')
        self.assertEqual(data['tutoring_options'][0]['id'], 1)
        self.assertEqual(len(data['writing_services']), 6)
        self.assertEqual(data['writing_services'][0]['name'], 'Application')
        self.assertEqual(data['writing_services'][0]['id'], 1)
        self.assertEqual(data['courses'], [
            {'id': 'TRAIN 100', 'name': 'TRAIN 100'},
            {'id': 'TRAIN 101', 'name': 'TRAIN 101'},
            {'id': 'PHYS 121', 'name': 'PHYS 121'},
        ])
