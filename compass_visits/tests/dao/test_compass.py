# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.dao.compass import CompassVisits, CompassVisitModel
from compass_visits.tests import CompassVisitsTestCase


class CompassVisitsTestCase(CompassVisitsTestCase):
    def test_get_ic_eligibility(self):
        compass = CompassVisits()
        eligible = compass.get_ic_eligibility("532353230")
        self.assertTrue(eligible)
        not_eligible = compass.get_ic_eligibility("000000000")
        self.assertFalse(not_eligible)

    def test_store_visit(self):
        compass = CompassVisits()
        visit = CompassVisitModel(
            student_syskey="532353230",
            visit_time=datetime.datetime(2024, 1, 1, 12, 0, 0),
            visit_type="in_person",
            visit_location="Smith Hall",
        )
        response = compass.store_visit(visit)
        self.assertTrue(response)
