# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db.models import Q
from django.utils import timezone
from compass_visits.exceptions import ValidationError
from compass_visits.models import (Visit,
                                   ProgramArea,
                                   TutoringOption,
                                   WritingService)


def get_active_visit_for_student(netid):
    # Return the active visit for the given netid,
    # or None if there is no active visit.
    try:
        return Visit.objects.filter(Q(check_out_date__isnull=True) |
                                    Q(is_verified=False)
                                    ).get(student_netid=netid)
    except Visit.DoesNotExist:
        return None


def validate_visit_data(request):
    program_area = request.get('program_area')
    tutoring_option = request.get('tutoring_option')
    writing_service = request.get('writing_service')
    course = request.get('course')

    if not program_area:
        raise ValidationError("program_area is required")
    if not tutoring_option:
        raise ValidationError("tutoring_option is required")
    if not (writing_service or course):
        raise ValidationError("Either writing_service or course is required")
    if writing_service and course:
        raise ValidationError("Only one of writing_service or"
                              " course can be provided")

    if not ProgramArea.objects.filter(id=program_area,
                                      allow_usage=True).exists():
        raise ValidationError("Invalid program_area")
    if not TutoringOption.objects.filter(id=tutoring_option,
                                         allow_usage=True).exists():
        raise ValidationError("Invalid tutoring_option")
    ws_exists = WritingService.objects.filter(id=writing_service,
                                              allow_usage=True).exists()
    if writing_service and not ws_exists:
        raise ValidationError("Invalid writing_service")


def create_visit_from_request(request_data, student_netid):
    active_visit = get_active_visit_for_student(student_netid)
    if active_visit is not None:
        raise ValidationError("Student already has an active visit")
    validate_visit_data(request_data)
    visit = Visit()
    visit.student_netid = student_netid
    visit.program_area = ProgramArea.objects.get(
        id=request_data['program_area'])
    visit.tutoring_option = TutoringOption.objects.get(
        id=request_data['tutoring_option'])
    if request_data.get('writing_service'):
        visit.writing_service = WritingService.objects.get(
            id=request_data['writing_service'])
    visit.course = request_data.get('course')
    visit.save()
    return visit


def update_visit(visit, request_data):
    if request_data.get('verify', False):
        visit.is_verified = True
    elif request_data.get('checkout', False):
        if not visit.is_verified:
            raise ValidationError("Visit must be verified before checkout")
        visit.check_out_date = timezone.now()
    visit.save()
    return visit


def get_total_hours_by_netid(netid):
    visits = Visit.objects.filter(student_netid=netid, is_verified=True)
    total_seconds = sum([
        (visit.check_out_date - visit.check_in_date).total_seconds()
        for visit in visits
        if visit.check_in_date and visit.check_out_date
    ])
    total_hours = total_seconds / 3600

    return total_hours
