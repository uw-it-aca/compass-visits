# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class ProgramArea(models.Model):
    name = models.CharField(max_length=255)
    allow_usage = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TutoringOption(models.Model):
    name = models.CharField(max_length=255)
    allow_usage = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class WritingService(models.Model):
    name = models.CharField(max_length=255)
    allow_usage = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Visit(models.Model):
    student_netid = models.CharField(max_length=255)
    program_area = models.ForeignKey(ProgramArea, on_delete=models.PROTECT)
    tutoring_option = models.ForeignKey(TutoringOption,
                                        on_delete=models.PROTECT)
    writing_service = models.ForeignKey(WritingService,
                                        on_delete=models.PROTECT,
                                        null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    check_in_date = models.DateTimeField(auto_now_add=True)
    check_out_date = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.student_netid} - {self.program_area.name} -"
                f" {self.check_in_date}")
