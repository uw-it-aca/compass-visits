# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import patch
from compass_visits.tests import CompassVisitsTestCase
from compass_visits.dao.pws import (get_student_photo,
                                    get_student_profile,
                                    get_regid_by_netid,
                                    get_syskey_by_netid,
                                    get_netid_by_syskey)
from restclients_core.exceptions import DataFailureException


class PWSDAOTest(CompassVisitsTestCase):
    def test_get_student_profile(self):
        profile = get_student_profile("javerage")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["netid"], "javerage")
        self.assertEqual(
            profile["uwregid"], "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEqual(profile["student_name"], "Jamesy McJamesy")
        self.assertEqual(profile["student_number"], "1033334")

    def test_get_student_photo(self):
        photo = get_student_photo("9136CCB8F66711D5BE060004AC494FFE")
        self.assertIsNotNone(photo)
        no_photo = get_student_photo("nonexistent")
        self.assertIsNone(no_photo)

    def test_get_regid_by_netid(self):
        regid = get_regid_by_netid("javerage")
        self.assertEqual(regid, "9136CCB8F66711D5BE060004AC494FFE")
        with self.assertRaises(DataFailureException):
            no_regid = get_regid_by_netid("nonexistent")
            self.assertIsNone(no_regid)

    def test_get_syskey_by_netid(self):
        syskey = get_syskey_by_netid("javerage")
        self.assertEqual(syskey, "000083856")
        with self.assertRaises(DataFailureException):
            no_syskey = get_syskey_by_netid("nonexistent")
            self.assertIsNone(no_syskey)

    def test_get_netid_by_syskey(self):
        netid = get_netid_by_syskey("000083856")
        self.assertEqual(netid, "javerage")
        with self.assertRaises(DataFailureException):
            no_netid = get_netid_by_syskey("000000000")
            self.assertIsNone(no_netid)

    def test_get_student_photo_none_person(self):
        with patch("compass_visits.dao.pws.PWS") as mock_pws:
            mock_pws.return_value.get_idcard_photo.side_effect = (
                DataFailureException(
                    '/student/v5/photo/someone', 404, 'Not Found'))
            result = get_student_photo("someone")
            self.assertIsNone(result)

    def test_get_student_photo_no_uwregid(self):
        with patch("compass_visits.dao.pws.PWS") as mock_pws:
            result = get_student_photo(None)
            mock_pws.assert_not_called()
            self.assertIsNone(result)

    def test_get_syskey_by_netid_none_person(self):
        with patch("compass_visits.dao.pws.PWS") as mock_pws:
            mock_pws.return_value.get_person_by_netid.return_value = None
            result = get_syskey_by_netid("someone")
            self.assertIsNone(result)

    def test_get_regid_by_netid_none_person(self):
        with patch("compass_visits.dao.pws.PWS") as mock_pws:
            mock_pws.return_value.get_person_by_netid.return_value = None
            result = get_regid_by_netid("someone")
            self.assertIsNone(result)
