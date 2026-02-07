# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass_visits.models import ProgramArea, TutoringOption, WritingService


def get_visit_options():
    # Return a dictionary containing the list of program areas, tutoring
    # options, and writing services. Each list should only include options
    # where allow_usage is True.
    program_areas = list(ProgramArea.objects.filter(allow_usage=True)
                         .values('id', 'name'))
    tutoring_options = list(TutoringOption.objects.filter(allow_usage=True)
                            .values('id', 'name'))
    writing_services = list(WritingService.objects.filter(allow_usage=True)
                            .values('id', 'name'))

    # TODO: Add SWS client and include student's course list in the response
    return {
        'program_areas': program_areas,
        'tutoring_options': tutoring_options,
        'writing_services': writing_services
    }
