# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.dao.compass import Compass, CompassVisitModel
from compass_visits.tests import CompassVisitsTestCase
import datetime


class CompassTestCase(CompassVisitsTestCase):
    def test_get_ic_eligibility(self):
        compass = Compass()
        eligible = compass.get_ic_eligibility("532353230")
        self.assertTrue(eligible)
        not_eligible = compass.get_ic_eligibility("000000000")
        self.assertFalse(not_eligible)

    def test_store_visit(self):
        compass = Compass()
        visit = CompassVisitModel(
            student_netid="javerage",
            visit_type="Virtual",
            course_code="STAT 101",
            tutoring_option="Individual",
            checkin_date=datetime.datetime.now(),
            checkout_date=datetime.datetime.now(),
        )
        response = compass.store_visit(visit)
        self.assertTrue(response)
        self.assertEqual(response["student_netid"], "javerage")
        self.assertEqual(response["visit_type"], "Virtual")
        self.assertEqual(response["course_code"], "STAT 101")
        self.assertEqual(response["tutoring_option"], "Individual")
