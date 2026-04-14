# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import CompassVisitsTestCase
from compass_visits.dao.sws import get_class_list
from compass_visits.dao.pws import get_regid_by_netid


class SWSDAOTest(CompassVisitsTestCase):
    def test_list(self):
        regid = get_regid_by_netid("javerage")
        class_list = get_class_list(regid)
        self.assertIsNotNone(class_list)
        self.assertEqual(len(class_list), 3)
        self.assertEqual(class_list[0], "TRAIN 100")
        self.assertEqual(class_list[1], "TRAIN 101")
        self.assertEqual(class_list[2], "PHYS 121")
