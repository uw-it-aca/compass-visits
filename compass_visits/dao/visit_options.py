# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.models import ProgramArea, TutoringOption, WritingService
from compass_visits.dao.sws import get_class_list


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
    program_areas = list(ProgramArea.objects.filter(allow_usage=True)
                         .values('id', 'name'))
    tutoring_options = list(TutoringOption.objects.filter(allow_usage=True)
                            .values('id', 'name'))
    writing_services = list(WritingService.objects.filter(allow_usage=True)
                            .values('id', 'name'))

    courses = get_class_list(student_regid)
    return {
        'program_areas': program_areas,
        'tutoring_options': tutoring_options,
        'writing_services': writing_services,
        'courses': courses
    }
