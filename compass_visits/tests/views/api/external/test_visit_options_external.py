# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.tests import APITokenTestCase
from compass_visits.dao.pws import get_regid_by_netid


class VisitOptionsExternalAPITestCase(APITokenTestCase):

    def test_get_options(self):
        response = self.get_response('visit_options_external',
                                     token='Token testtoken',
                                     url_args={'student_regid': '000083856'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('program_areas', data)
        self.assertIn('tutoring_options', data)
        self.assertIn('writing_services', data)
        self.assertIn('courses', data)
        self.assertEqual((len(data['courses'])), 0)

        regid = get_regid_by_netid("javerage")
        response = self.get_response('visit_options_external',
                                     token='Token testtoken',
                                     url_args={'student_regid': regid})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual((len(data['courses'])), 3)
        self.assertEqual(data['courses'][0], {"id": "TRAIN 100",
                                              "name": "TRAIN 100"})
