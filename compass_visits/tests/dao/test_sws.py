# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime
from types import SimpleNamespace
from unittest.mock import patch

from compass_visits.dao.pws import get_regid_by_netid
from compass_visits.dao.sws import (
    get_class_list_from_registrations,
    get_term_start_date,
)
from compass_visits.tests import CompassVisitsTestCase


class SWSDAOTest(CompassVisitsTestCase):
    def test_list(self):
        regid = get_regid_by_netid("javerage")
        class_list = get_class_list_from_registrations(regid)
        self.assertIsNotNone(class_list)
        self.assertEqual(len(class_list), 3)
        self.assertEqual(class_list[0], {"id": "TRAIN 100",
                                         "name": "TRAIN 100"})
        self.assertEqual(class_list[1], {"id": "TRAIN 101",
                                         "name": "TRAIN 101"})
        self.assertEqual(class_list[2], {"id": "PHYS 121",
                                         "name": "PHYS 121"})

    @patch('compass_visits.dao.sws.get_resource')
    @patch('compass_visits.dao.sws.get_current_term')
    def test_list_from_paginated_registrations(self, mock_current_term,
                                                mock_get_resource):
        mock_current_term.return_value = SimpleNamespace(
            quarter='autumn', year=2026)
        mock_get_resource.side_effect = [
            {
                'Registrations': [
                    {'Section': {
                        'CurriculumAbbreviation': 'MATH',
                        'CourseNumber': '124',
                    }},
                    {'Section': {
                        'CurriculumAbbreviation': 'MATH',
                        'CourseNumber': '124',
                    }},
                ],
                'Next': {'Href': '/student/v5/registration.json?page=2'},
            },
            {
                'Registrations': [{
                    'CurriculumAbbreviation': 'ENGL',
                    'CourseNumber': '131',
                }],
                'Next': None,
            },
        ]

        class_list = get_class_list_from_registrations('test-regid')

        self.assertEqual(class_list, [
            {'id': 'MATH 124', 'name': 'MATH 124'},
            {'id': 'ENGL 131', 'name': 'ENGL 131'},
        ])
        self.assertEqual(mock_get_resource.call_count, 2)
        self.assertEqual(
            mock_get_resource.call_args_list[1].args,
            ('/student/v5/registration.json?page=2',),
        )

    def test_term(self):
        start_date = get_term_start_date()
        self.assertIsNotNone(start_date)
        self.assertTrue(isinstance(start_date, datetime.datetime))
        self.assertEqual(start_date.date(), datetime.date(2013, 4, 1))
