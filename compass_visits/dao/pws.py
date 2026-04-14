# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_pws import PWS
from restclients_core.exceptions import DataFailureException


PHOTO_SIZE = "large"


def get_student_profile(uwnetid):
    pws = PWS()
    person = pws.get_person_by_netid(uwnetid)
    if person is None:
        return None
    return {
        "netid": uwnetid,
        "student_name": person.display_name,
        "student_number": person.student_number,
        "student_syskey": person.student_system_key
    }


def get_student_photo(uwnetid):
    pws = PWS()
    try:
        person = pws.get_person_by_netid(uwnetid)
        return pws.get_idcard_photo(person.uwregid, size=PHOTO_SIZE)
    except DataFailureException:
        return None


def get_syskey_by_netid(uwnetid):
    pws = PWS()
    person = pws.get_person_by_netid(uwnetid)
    if person is None:
        return None
    return person.student_system_key
