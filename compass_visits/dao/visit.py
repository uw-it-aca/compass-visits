# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db.models import Q
from compass_visits.models import Visit


def get_active_visit_for_student(netid):
    # Return the active visit for the given netid,
    # or None if there is no active visit.
    try:
        return Visit.objects.filter(Q(check_out_date__isnull=True) |
                                    Q(is_verified=False)
                                    ).get(student_netid=netid)
    except Visit.DoesNotExist:
        return None
