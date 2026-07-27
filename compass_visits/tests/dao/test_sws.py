# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime

from compass_visits.dao.pws import get_regid_by_netid
from compass_visits.dao.sws import get_class_list, get_term_start_date
from compass_visits.tests import CompassVisitsTestCase


class SWSDAOTest(CompassVisitsTestCase):
    def test_list(self):
        regid = get_regid_by_netid("javerage")
        class_list = get_class_list(regid)
        self.assertIsNotNone(class_list)
        self.assertEqual(len(class_list), 3)
        self.assertEqual(class_list[0], {"id": "TRAIN 100",
                                         "name": "TRAIN 100"})
        self.assertEqual(class_list[1], {"id": "TRAIN 101",
                                         "name": "TRAIN 101"})
        self.assertEqual(class_list[2], {"id": "PHYS 121",
                                         "name": "PHYS 121"})

    def test_term(self):
        start_date = get_term_start_date()
        self.assertIsNotNone(start_date)
        self.assertTrue(isinstance(start_date, datetime.datetime))
        self.assertEqual(start_date.date(), datetime.date(2013, 4, 1))
