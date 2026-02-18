# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('loaddata', 'initial_data/program-area.json')
        call_command('loaddata', 'initial_data/tutoring-option.json')
        call_command('loaddata', 'initial_data/writing-service.json')

        # must be last for FKs to line up
        call_command('loaddata', 'initial_data/visit.json')
