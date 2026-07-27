# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os

from django.apps import AppConfig
from django.contrib.staticfiles.apps import StaticFilesConfig
from restclients_core.dao import MockDAO


class ViteStaticFilesConfig(StaticFilesConfig):
    ignore_patterns = ['CVS', '*~']


class CompassVisitsConfig(AppConfig):
    name = "compass_visits"

    def ready(self):
        compass_visits_mocks = os.path.join(os.path.dirname(__file__),
                                            "resources")
        MockDAO.register_mock_path(compass_visits_mocks)
