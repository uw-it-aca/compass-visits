# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import CompassVisitsTestCase
from compass_visits.dao.visit_options import get_visit_options


class VisitOptionsTestCase(CompassVisitsTestCase):
    def test_get_visit_options(self):
        options = get_visit_options()
        self.assertIn('program_areas', options)
        self.assertIn('tutoring_options', options)
        self.assertIn('writing_services', options)
        self.assertIsInstance(options['program_areas'], list)
        self.assertIsInstance(options['tutoring_options'], list)
        self.assertIsInstance(options['writing_services'], list)

        self.assertEqual(len(options['program_areas']), 8)
        self.assertEqual(options['program_areas'][0]['name'],
                         'Biology/Natural Sci')
        self.assertEqual(options['program_areas'][0]['id'], 1)

        self.assertEqual(len(options['tutoring_options']), 2)
        self.assertEqual(options['tutoring_options'][0]['name'], 'Drop In')
        self.assertEqual(options['tutoring_options'][0]['id'], 1)

        self.assertEqual(len(options['writing_services']), 6)
        self.assertEqual(options['writing_services'][0]['name'],
                         'Application')
        self.assertEqual(options['writing_services'][0]['id'], 1)
