# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import CompassVisitsTestCase
from compass_visits.dao.pws import get_student_photo, get_student_profile


class PWSDAOTest(CompassVisitsTestCase):
    def test_get_student_profile(self):
        profile = get_student_profile("javerage")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["netid"], "javerage")
        self.assertEqual(profile["student_name"], "Jamesy McJamesy")
        self.assertEqual(profile["student_number"], "1033334")

    def test_get_student_photo(self):
        photo = get_student_photo("javerage")
        self.assertIsNotNone(photo)
        no_photo = get_student_photo("nonexistent")
        self.assertIsNone(no_photo)
