# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.cache import cache
from restclients_core.exceptions import DataFailureException

from compass_visits.dao.compass import Compass
from compass_visits.dao.sws import get_class_list_from_registrations
from compass_visits.models import WritingService

COMPASS_VISIT_CATALOG_CACHE_KEY = 'compass_visit_catalog'
COMPASS_VISIT_CATALOG_CACHE_SECONDS = 60 * 60


def get_compass_visit_catalog():
    catalog = cache.get(COMPASS_VISIT_CATALOG_CACHE_KEY)
    if catalog is None:
        catalog = Compass().get_visit_catalog()
        cache.set(COMPASS_VISIT_CATALOG_CACHE_KEY,
                  catalog,
                  COMPASS_VISIT_CATALOG_CACHE_SECONDS)
    return catalog


def get_visit_options(student_regid):
    """
    Retrieves available visit options for program areas, tutoring, and
    writing services.

    Returns:
        dict: A dictionary containing three keys:
            - 'program_areas': List of dictionaries with 'id' and 'name' of
                               program areas where allow_usage is True.
            - 'tutoring_options': List of dictionaries with 'id' and 'name' of
                                  tutoring options where allow_usage is True.
            - 'writing_services': List of dictionaries with 'id' and 'name' of
                                  writing services where allow_usage is True.

    Note:
        Only options with allow_usage set to True are included in the lists.
    """
    writing_services = list(WritingService.objects.filter(allow_usage=True)
                            .values('id', 'name'))
    try:
        courses = get_class_list_from_registrations(student_regid)
    except DataFailureException:
        courses = []

    try:
        catalog = get_compass_visit_catalog()
    except DataFailureException:
        catalog = {'visit_types': [], 'tutoring_options': []}

    return {
        'program_areas': catalog.get('visit_types', []),
        'tutoring_options': catalog.get('tutoring_options', []),
        'writing_services': writing_services,
        'courses': courses,
    }
