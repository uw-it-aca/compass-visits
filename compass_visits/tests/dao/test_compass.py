# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime

from restclients_core.exceptions import DataFailureException

from compass_visits.dao.compass import Compass, CompassVisitModel
from compass_visits.tests import CompassVisitsTestCase


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
            checkin_date=datetime.datetime.now(tz=datetime.timezone.utc),
            checkout_date=datetime.datetime.now(tz=datetime.timezone.utc),
        )
        response = compass.store_visit(visit)
        self.assertTrue(response)
        self.assertEqual(response["student_netid"], "javerage")
        self.assertEqual(response["visit_type"], "Virtual")
        self.assertEqual(response["course_code"], "STAT 101")
        self.assertEqual(response["tutoring_option"], "Individual")

    def test_get_current_quarter_visits(self):
        compass = Compass()
        visits = compass.get_current_quarter_visits("000083856")
        self.assertEqual(len(visits), 3)
        self.assertIsInstance(visits[0], CompassVisitModel)
        self.assertEqual(visits[0].student_netid, "javerage")

    def test_get_current_quarter_visits_empty(self):
        compass = Compass()
        visits = compass.get_current_quarter_visits("000012345")
        self.assertEqual(visits, [])

    def test_get_current_quarter_visits_datafailure(self):
        compass = Compass()
        with self.assertRaises(DataFailureException):
            compass.get_current_quarter_visits("000000000")

    def test_visit_json_data_with_none_checkout_date(self):
        checkin = datetime.datetime(2026, 7, 6, 12, 30, 0, tzinfo=datetime.timezone.utc)
        visit = CompassVisitModel(
            student_netid="javerage",
            visit_type="Virtual",
            course_code="STAT 101",
            tutoring_option="Individual",
            checkin_date=checkin,
            checkout_date=None,
        )

        data = visit.json_data()

        self.assertEqual(data["checkin_date"], checkin.isoformat())
        self.assertIsNone(data["checkout_date"])
