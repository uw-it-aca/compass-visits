# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.utils import timezone


class ProgramArea(models.Model):
    """
    Represents a program area within the system.

    Attributes:
        name (CharField): The name of the program area.
        allow_usage (BooleanField): Indicates whether the program area is
        allowed for usage. Defaults to True.
    """
    name = models.CharField(max_length=255)
    allow_usage = models.BooleanField(default=True)


class TutoringOption(models.Model):
    """
    Represents an option for tutoring services.

    Attributes:
        name (CharField): The name of the tutoring option.
        allow_usage (BooleanField): Indicates whether the tutoring option is
        allowed for usage. Defaults to True.
    """
    name = models.CharField(max_length=255)
    allow_usage = models.BooleanField(default=True)


class WritingService(models.Model):
    """
    Represents a writing service that can be used within the application.

    Attributes:
        name (CharField): The name of the writing service.
        allow_usage (BooleanField): Indicates whether the writing service is
        allowed for usage. Defaults to True.
    """
    name = models.CharField(max_length=255)
    allow_usage = models.BooleanField(default=True)


class Visit(models.Model):
    """
    Represents a student visit record in the Compass Visits system.

    Fields:
        student_netid (CharField): The NetID of the student.
        program_area (ForeignKey): Reference to the ProgramArea.
        tutoring_option (ForeignKey): Reference to the TutoringOption.
        writing_service (ForeignKey, optional): Reference to the
                                                WritingService used, if any.
        course (CharField, optional): The course associated with the visit,
                                      if applicable.
        check_in_date (DateTimeField): Timestamp when the student checked in
                                       (auto-set on creation).
        check_out_date (DateTimeField, optional): Timestamp when the student
                                                  checked out.
        is_verified (BooleanField): Indicates whether the visit IS verified.

    Methods:
        json_data(): Returns a dictionary representation of the visit suitable
                     for JSON serialization.
    """
    student_netid = models.CharField(max_length=255, db_index=True)
    program_area = models.ForeignKey(ProgramArea, on_delete=models.PROTECT)
    tutoring_option = models.ForeignKey(TutoringOption,
                                        on_delete=models.PROTECT)
    writing_service = models.ForeignKey(WritingService,
                                        on_delete=models.PROTECT,
                                        null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    check_in_date = models.DateTimeField(default=timezone.now, db_index=True)
    check_out_date = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def json_data(self):
        return {
            "id": self.id,
            "student_netid": self.student_netid,
            "program_area": self.program_area.name,
            "tutoring_option": self.tutoring_option.name,
            "writing_service": self.writing_service.name if
            self.writing_service else None,
            "course": self.course,
            "check_in_date": self.check_in_date.isoformat(),
            "check_out_date": self.check_out_date.isoformat() if
            self.check_out_date else None,
            "is_verified": self.is_verified,
        }
