# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db.models import Q
from django.utils import timezone, dateparse
from compass_visits.exceptions import ValidationError
from django.db.models import F, ExpressionWrapper, DurationField, Sum
from compass_visits.models import (Visit,
                                   ProgramArea,
                                   TutoringOption,
                                   WritingService)
from compass_visits.dao.sws import get_term_start_date


def get_active_visit_for_student(student_syskey):
    """
    Retrieve the active visit for a given student's syskey.

    An active visit is defined as a visit where either the check-out date is
    null or the visit is not verified. If multiple active visits are found,
    the most recent one (by check-in date) is returned. If no active visit
    exists, returns None.

    Args:
        student_syskey (str): The SysKey of the student.

    Returns:
        Visit or None: The active Visit object for the student, or None if
            not found.
    """
    try:
        return Visit.objects.filter(Q(check_out_date__isnull=True) |
                                    Q(is_verified=False)
                                    ).get(student_syskey=student_syskey)
    except Visit.DoesNotExist:
        return None
    except Visit.MultipleObjectsReturned:
        return (Visit.objects.filter(Q(check_out_date__isnull=True) |
                                     Q(is_verified=False),
                                     student_syskey=student_syskey)
                .latest('check_in_date'))


def get_student_state(active_visit):
    """
    Determines the state of a student's visit based on the provided
    active_visit object.

    Args:
        active_visit: An object representing the student's current visit.
        It is expected to have the attributes 'is_verified' (bool) and
        'check_out_date' (datetime or None).

    Returns:
        str: The state of the student's visit, which can be:
            - "none": No active visit or the visit has ended.
            - "pending_verification": The visit is not yet verified.
            - "active": The visit is verified and currently active
    """

    if not active_visit:
        return "none"
    if not active_visit.is_verified:
        return "pending_verification"
    if active_visit.check_out_date is None:
        return "active"
    return "none"


def validate_visit_data(request):
    """
    Validates the visit data provided in the request dictionary.

    This function checks for the presence and validity of required fields:
    - 'program_area' must be provided and correspond to a ProgramArea
    - 'tutoring_option' must be provided and correspond to a TutoringOption.
    - Either 'writing_service' or 'course' must be provided, but not both.
    - If 'writing_service' is provided it must correspond to a WritingService.

    Raises:
        ValidationError: If any required field is missing, if both or neither
                         'writing_service' and 'course' are provided,  or if
                         any provided ID does not correspond to an allowed
                         object.
    """
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


def create_visit_from_request(request_data, student_syskey, verified=False):
    """
    Creates a new Visit instance from the provided request data for a given
    student.

    This function first checks if the student already has an active visit and
    raises a ValidationError if so. It then validates the request data,
    creates a new Visit object, and populates its fields based on the request
    data.
    Finally, it saves the Visit instance to the database and returns it.

    Args:
        request_data (dict): Dictionary containing visit details,
                             including 'program_area', 'tutoring_option',
                             and optionally 'writing_service' and 'course'.
        student_syskey (str): The SysKey of the student for whom the visit
                             is being created.

    Returns:
        Visit: The newly created Visit instance.

    Raises:
        ValidationError: If the student already has an active visit or if
            the request data is invalid.
        ProgramArea.DoesNotExist: If the specified ProgramArea does not exist.
        TutoringOption.DoesNotExist: If the specified TutoringOption does
            not exist.
        WritingService.DoesNotExist: If the specified WritingService does
            not exist (when provided).
    """
    active_visit = get_active_visit_for_student(student_syskey)
    if active_visit is not None:
        raise ValidationError("Student already has an active visit")
    validate_visit_data(request_data)
    visit = Visit()
    visit.student_syskey = student_syskey
    visit.program_area = ProgramArea.objects.get(
        id=request_data['program_area'])
    visit.tutoring_option = TutoringOption.objects.get(
        id=request_data['tutoring_option'])
    if request_data.get('writing_service'):
        visit.writing_service = WritingService.objects.get(
            id=request_data['writing_service'])
    visit.course = request_data.get('course')
    visit.is_verified = verified
    visit.save()
    return visit


def student_update_visit(visit, request_data):
    """
    Updates a student's visit record based on the provided request data.

    If the 'checkout' key in request_data is True, this function attempts to
    check out the visit. It raises a ValidationError if the visit is already
    checked out or if the visit has not been verified. If checkout is
    successful, the current time is set as the check_out_date.

    Args:
        visit: The visit instance to update.
        request_data (dict): Data containing update instructions, expects a
        'checkout' boolean key.

    Returns:
        The updated visit instance.

    Raises:
        ValidationError: If the visit is already checked out or has not been
        verified before checkout.
    """

    if request_data.get('checkout', False):
        if visit.check_out_date:
            raise ValidationError("Visit is already checked out")
        if not visit.is_verified:
            raise ValidationError("Visit must be verified before checkout")
        visit.check_out_date = timezone.now()
    visit.save()
    return visit


def manager_update_visit(visit, request_data):
    """
    Updates a visit instance based on manager actions specified in the\
    request data.

    This function allows a manager to verify a visit and/or perform a
    checkout operation.
    - If 'verify' is True in request_data, the visit will be marked as
        verified unless it is already verified.
    - If 'checkout' is True in request_data, the visit will be checked out
        (check_out_date set to now) only if it is already verified and not
        already checked out.

    Args:
        visit: The Visit model instance to be updated.
        request_data (dict): Dictionary containing actions. Supported keys:
            - 'verify' (bool): Whether to verify the visit.
            - 'checkout' (bool): Whether to check out the visit.

    Raises:
        ValidationError: If attempting to verify an already verified visit,
                         if attempting to check out a visit that is not
                         verified, or if the visit is already checked out.

    Returns:
        The updated Visit instance.
    """
    if request_data.get('verify', False):
        if visit.is_verified:
            raise ValidationError("Visit is already verified")
        visit.is_verified = True
    if request_data.get('checkout', False):
        if not visit.is_verified:
            raise ValidationError("Visit must be verified before checkout")
        if visit.check_out_date:
            raise ValidationError("Visit is already checked out")
        visit.check_out_date = timezone.now()
    visit.save()
    return visit


def manager_create_visit_from_request(request_data):
    """
    Creates and saves a Visit instance from the provided request data.

    Validates the input data, retrieves related objects, sets Visit fields,
    and handles optional verification and checkout logic.

    Args:
        request_data (dict): Dictionary containing visit data. Expected keys:
            - 'student_syskey' (str): SysKey of the student (required).
            - 'program_area' (int): ID of the ProgramArea (required).
            - 'tutoring_option' (int): ID of the TutoringOption (required).
            - 'writing_service' (int, optional): ID of the WritingService.
            - 'verify' (bool, optional): If True, marks the visit as verified.
            - 'check_in_date' (datetime, optional): Check-in date for the
                                                    visit. Defaults to now.
            - 'checkout' (bool, optional): If True, marks the visit as
                    verified and sets check_out_date.
            - 'course' (str, optional): Course information.

    Returns:
        Visit: The created and saved Visit instance.

    Raises:
        ValidationError: If required fields are missing or invalid.
        ProgramArea.DoesNotExist: If the specified ProgramArea does not exist.
        TutoringOption.DoesNotExist: If the specified TutoringOption does not
                                     exist.
        WritingService.DoesNotExist: If the specified WritingService does not
                                     exist.
    """
    validate_visit_data(request_data)
    visit = Visit()
    visit.student_syskey = request_data.get('student_syskey')
    if not visit.student_syskey:
        raise ValidationError("student_syskey is required")
    if request_data.get('check_in_date'):
        try:
            visit.check_in_date = dateparse.parse_datetime(
                request_data['check_in_date'])
        except (ValueError, TypeError):
            raise ValidationError("Invalid check_in_date format")
    try:
        visit.program_area = ProgramArea.objects.get(
            id=request_data['program_area'])
        visit.tutoring_option = TutoringOption.objects.get(
            id=request_data['tutoring_option'])
        if request_data.get('writing_service'):
            visit.writing_service = WritingService.objects.get(
                id=request_data['writing_service'])
    except ProgramArea.DoesNotExist:
        raise ValidationError("Invalid program_area")
    except TutoringOption.DoesNotExist:
        raise ValidationError("Invalid tutoring_option")
    except WritingService.DoesNotExist:
        raise ValidationError("Invalid writing_service")
    if request_data.get('verify', False):
        visit.is_verified = True
    if request_data.get('checkout', False):
        visit.is_verified = True
        visit.check_out_date = timezone.now()
    visit.course = request_data.get('course')
    visit.save()
    return visit


def get_total_minutes_by_syskey(student_syskey):
    """
    Calculates the total completed visit minutes for a student by SysKey.

    Args:
        student_syskey (str): The SysKey of the student to calculate total
            minutes for.

    Returns:
        float: The total number of minutes as a float
    Notes:
        - Only visits with both check-in and check-out dates are considered.
        - Only visits marked as verified (is_verified=True) are included.
    """
    visits = Visit.objects.filter(
        student_syskey=student_syskey,
        is_verified=True,
        check_in_date__isnull=False,
        check_out_date__isnull=False
    ).annotate(
        duration=ExpressionWrapper(
            F('check_out_date') - F('check_in_date'),
            output_field=DurationField()
        )
    )
    total_duration = visits.aggregate(total=Sum('duration'))['total']
    if total_duration is None:
        return 0.0
    return total_duration.total_seconds() / 60


def get_visits_pending_verification():
    """
    Retrieve all Visit objects that are pending verification.

    Returns:
        QuerySet: A Django QuerySet containing Visit instances where
                  'is_verified' is False.
    """
    return Visit.objects.select_related(
        'program_area', 'tutoring_option', 'writing_service'
    ).filter(is_verified=False)


def get_visits_pending_checkout():
    """
    Retrieve all Visit objects that are pending checkout.

    Returns:
        QuerySet: A Django QuerySet containing Visit instances where
                  'is_verified' is True and 'check_out_date' is null.
    """
    return Visit.objects.select_related(
        'program_area', 'tutoring_option', 'writing_service'
    ).filter(is_verified=True, check_out_date__isnull=True)


def get_completed_visits_by_syskey(student_syskey):
    """
    Retrieve all completed Visit objects for a student by SysKey.

    Args:
        student_syskey (str): The SysKey of the student to retrieve completed
            visits for.

    Returns:
        QuerySet: A Django QuerySet containing Visit instances where
                  'is_verified' is True and 'check_out_date' is not null,
                  ordered by 'check_in_date' in descending order.
    """
    return (Visit.objects.select_related(
        'program_area', 'tutoring_option', 'writing_service'
    ).filter(student_syskey=student_syskey, is_verified=True,
             check_out_date__isnull=False)
        .order_by('-check_in_date'))


def get_current_quarter_visits_by_syskey(student_syskey):
    """
    Retrieve all Visit objects for a student by SysKey that have a check-in
    date within the current quarter.
    Args:
        student_syskey (str): The SysKey of the student to retrieve visits for.
    Returns:
        QuerySet: A Django QuerySet containing Visit instances where
                    'student_syskey' matches the provided SysKey and
                    'check_in_date'is greater than or equal to the start date
                    of the current quarter, ordered by 'check_in_date' in
                    descending order.
    """
    current_term_start = get_term_start_date()
    visits = (Visit.objects
              .select_related('program_area',
                              'tutoring_option',
                              'writing_service')
              .filter(student_syskey=student_syskey,
                      check_in_date__gte=current_term_start)
              .order_by('-check_in_date'))
    return visits


def checkout_active_verified_visit(student_syskey):
    """
    Checks out the active verified visit for a student by setting the
    check_out_date to the current time.

    This function looks for an active visit that is verified (is_verified=True)
    and has no check_out_date. If such a visit exists, it updates the
    check_out_date to the current time. If no such visit exists, it does
    nothing.

    Args:
        student_syskey (str): The SysKey of the student whose visit should be
            checked out.
    Returns:
        bool: True if a visit was checked out, False if no active verified
            visit was found.
    """

    updated_count = Visit.objects.filter(student_syskey=student_syskey,
                                         is_verified=True,
                                         check_out_date=None)\
        .update(check_out_date=timezone.now())
    return updated_count > 0
