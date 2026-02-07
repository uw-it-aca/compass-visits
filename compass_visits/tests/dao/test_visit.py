# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import CompassVisitsTestCase
from compass_visits.dao.visit import get_active_visit_for_student


class VisitDAOTest(CompassVisitsTestCase):
    def test_get_active_visit_for_student(self):
        netid = "asmith"
        visit = get_active_visit_for_student(netid)
        self.assertIsNotNone(visit)

        netid = "javerage"
        visit = get_active_visit_for_student(netid)
        self.assertIsNone(visit)
