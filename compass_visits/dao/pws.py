# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_pws import PWS
from restclients_core.exceptions import DataFailureException, InvalidRegID

PHOTO_SIZE = "large"


def get_student_profile(uwnetid):
    pws = PWS()
    person = pws.get_person_by_netid(uwnetid)
    if person is None:
        return None
    return {
        "netid": uwnetid,
        "uwregid": person.uwregid,
        "student_name": person.display_name,
        "student_number": person.student_number,
        "student_syskey": person.student_system_key
    }


def get_student_photo(uwregid):
    if not uwregid:
        return None
    pws = PWS()
    try:
        return pws.get_idcard_photo(uwregid, size=PHOTO_SIZE)
    except (DataFailureException, InvalidRegID):
        return None


def get_syskey_by_netid(uwnetid):
    pws = PWS()
    person = pws.get_person_by_netid(uwnetid)
    if person is None:
        return None
    return person.student_system_key


def get_regid_by_netid(uwnetid):
    pws = PWS()
    person = pws.get_person_by_netid(uwnetid)
    if person is None:
        return None
    return person.uwregid


def get_netid_by_syskey(student_syskey):
    pws = PWS()
    persons = pws.person_search(student_system_key=student_syskey)
    if persons:
        return persons[0].uwnetid
