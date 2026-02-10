# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class CompassVisitsTestCase(TestCase):
    fixtures = ['initial_data/program-area.json',
                'initial_data/tutoring-option.json',
                'initial_data/writing-service.json',
                'initial_data/visit.json']


class APITestCase(CompassVisitsTestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0',
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def _set_user(self, netid):
        if netid is not None:
            self.client.force_login(User.objects.get_or_create(
                username=netid)[0])

    def get_response(self, url_name, url_args=None, netid=None,
                     method='get', data=None):
        self._set_user(netid)
        url = reverse(url_name, kwargs=url_args)
        return self.client.get(url, data)

    def post_response(self, url_name, netid=None, data=None):
        self._set_user(netid)
        url = reverse(url_name)
        return self.client.post(url, data, content_type='application/json')

    def patch_response(self, url_name, url_args=None, netid=None, data=None):
        self._set_user(netid)
        url = reverse(url_name, kwargs=url_args)
        return self.client.patch(url, data, content_type='application/json')

    def delete_response(self, url_name, url_args=None, netid=None, data=None):
        self._set_user(netid)
        url = reverse(url_name, kwargs=url_args)
        return self.client.delete(url, data, content_type='application/json')
