# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from compass_visits.exceptions import ValidationError
from django.utils import timezone


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

    @classmethod
    def create_from_request(cls, request_data, student_netid):
        visit = cls()
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

    def update_visit(self, request_data):
        if request_data.get('verify', False):
            self.is_verified = True
        elif request_data.get('checkout', False):
            if not self.is_verified:
                raise ValidationError("Visit must be verified before checkout")
            self.check_out_date = timezone.now()
        self.save()
