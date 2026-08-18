# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import datetime
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

from uw_sws import get_resource
from uw_sws.registration import get_schedule_by_regid_and_term
from uw_sws.term import get_current_term


def get_class_list(regid):
    term = get_current_term()
    schedule = get_schedule_by_regid_and_term(regid, term)
    class_list = []
    if schedule and schedule.sections:
        for section in schedule.sections:
            if section.is_primary_section:
                section_label = f"{section.curriculum_abbr} {section.course_number}"
                class_list.append({'id': section_label, 'name': section_label})
    return class_list


def get_class_list_from_registrations(regid):
    term = get_current_term()
    url = '/student/v5/registration.json?{}'.format(urlencode({
        'reg_id': regid,
        'quarter': term.quarter,
        'is_active': 'true',
        'year': term.year,
    }))
    class_list = []
    course_labels = set()

    while url:
        registrations = get_resource(url)
        for registration in registrations.get('Registrations', []):
            section = registration.get('Section', registration)
            section_label = '{} {}'.format(
                section['CurriculumAbbreviation'], section['CourseNumber'])
            if section_label not in course_labels:
                course_labels.add(section_label)
                class_list.append({'id': section_label, 'name': section_label})

        next_page = registrations.get('Next')
        url = next_page.get('Href') if next_page else None

    return class_list


def get_term_start_date():
    term = get_current_term()
    if term.first_day_quarter is not None:
        first_day = term.first_day_quarter
        first_day_datetime = datetime.datetime.combine(first_day,
                                                       datetime.time.max)
        zone = ZoneInfo("America/Los_Angeles")
        return first_day_datetime.astimezone(zone)
