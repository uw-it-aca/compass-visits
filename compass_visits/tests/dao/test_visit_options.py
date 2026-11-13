# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.dao.pws import get_regid_by_netid
from compass_visits.dao.visit_options import get_visit_options
from compass_visits.tests import CompassVisitsTestCase


class VisitOptionsTestCase(CompassVisitsTestCase):
    def test_get_visit_options(self):
        regid = get_regid_by_netid("javerage")
        options = get_visit_options(regid)
        self.assertIn('program_areas', options)
        self.assertIn('tutoring_options', options)
        self.assertIn('writing_services', options)
        self.assertIn('courses', options)
        self.assertIsInstance(options['program_areas'], list)
        self.assertIsInstance(options['tutoring_options'], list)
        self.assertIsInstance(options['writing_services'], list)
        self.assertIsInstance(options['courses'], list)

        self.assertEqual(len(options['program_areas']), 3)
        self.assertEqual(options['program_areas'][0]['name'],
                 'IC Drop-In Tutoring')
        self.assertEqual(options['program_areas'][0]['id'], 1)

        self.assertEqual(len(options['tutoring_options']), 3)
        self.assertEqual(options['tutoring_options'][0]['name'], 'Drop In')
        self.assertEqual(options['tutoring_options'][0]['id'], 1)

        self.assertEqual(len(options['writing_services']), 6)
        self.assertEqual(options['writing_services'][0]['name'],
                         'Application')
        self.assertEqual(options['writing_services'][0]['id'], 1)

        self.assertEqual(len(options['courses']), 3)
        self.assertEqual(options['courses'][0], {"id": "TRAIN 100",
                                                 "name": "TRAIN 100"})
        self.assertEqual(options['courses'][1], {"id": "TRAIN 101",
                                                 "name": "TRAIN 101"})
        self.assertEqual(options['courses'][2], {"id": "PHYS 121",
                                                 "name": "PHYS 121"})
