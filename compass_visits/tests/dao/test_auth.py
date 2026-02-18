# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.utils import timezone
from django.core.exceptions import PermissionDenied
from compass_visits.exceptions import ValidationError, OverrideNotPermitted
from compass_visits.tests import CompassVisitsTestCase
from compass_visits.dao.auth import (valid_user_override,
                                     can_write_visit,
                                     validate_token)
from unittest.mock import patch


class AuthDAOTest(CompassVisitsTestCase):

    @patch('userservice.user.UserService.get_override_user')
    def test_valid_user_override(self, mock_get_override_user):
        with self.settings(ALLOW_USER_OVERRIDE_FOR_WRITE=False):
            mock_get_override_user.return_value = 'javerage'
            with self.assertRaises(OverrideNotPermitted):
                valid_user_override()

            mock_get_override_user.return_value = None
            try:
                valid_user_override()
            except OverrideNotPermitted:
                self.fail("valid_user_override raised OverrideNotPermitted"
                          " unexpectedly!")

        with self.settings(ALLOW_USER_OVERRIDE_FOR_WRITE=True):
            mock_get_override_user.return_value = 'javerage'
            try:
                valid_user_override()
            except OverrideNotPermitted:
                self.fail("valid_user_override raised OverrideNotPermitted "
                          "unexpectedly!")
            mock_get_override_user.return_value = None
            try:
                valid_user_override()
            except OverrideNotPermitted:
                self.fail("valid_user_override raised OverrideNotPermitted "
                          "unexpectedly!")

    @patch('userservice.user.UserService.get_user')
    def test_can_write_visit(self, mock_get_user):
        mock_get_user.return_value = 'javerage'
        try:
            can_write_visit('javerage')
        except PermissionDenied:
            self.fail("can_write_visit raised PermissionDenied unexpectedly!")

        with self.assertRaises(PermissionDenied):
            can_write_visit('otheruser')

    def test_validate_token(self):
        with self.settings(EXTERNAL_API_TOKEN='validtoken'):
            with self.assertRaises(PermissionDenied):
                validate_token(None)

            with self.assertRaises(PermissionDenied):
                validate_token('InvalidFormat')

            with self.assertRaises(PermissionDenied):
                validate_token('Token invalidtoken')

            try:
                validate_token('Token validtoken')
            except PermissionDenied:
                self.fail("validate_token raised PermissionDenied"
                          " unexpectedly!")
