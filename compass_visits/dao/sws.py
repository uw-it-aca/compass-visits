# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_sws.term import get_current_term
from uw_sws.registration import get_schedule_by_regid_and_term
import datetime
from zoneinfo import ZoneInfo


def get_class_list(regid):
    term = get_current_term()
    schedule = get_schedule_by_regid_and_term(regid, term)
    class_list = []
    if schedule and schedule.sections:
        for section in schedule.sections:
            if section.is_primary_section:
                section_label = "{} {}".format(section.curriculum_abbr,
                                               section.course_number)
                class_list.append({'id': section_label, 'name': section_label})
    return class_list


def get_term_start_date():
    term = get_current_term()
    if term.first_day_quarter is not None:
        first_day = term.first_day_quarter
        first_day_datetime = datetime.datetime.combine(first_day,
                                                       datetime.time.max)
        zone = ZoneInfo("America/Los_Angeles")
        return first_day_datetime.astimezone(zone)
