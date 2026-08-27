# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django management command to initialize the database with initial data.

    This command loads fixture data for writing services followed by visit
    data.

    Usage:
        python manage.py initialize_db

    The fixtures are loaded in the following order:
        1. initial_data/writing-service.json
        2. initial_data/visit.json
    """
    def handle(self, *args, **options):
        call_command('loaddata', 'initial_data/writing-service.json')
        call_command('loaddata', 'initial_data/visit.json')
