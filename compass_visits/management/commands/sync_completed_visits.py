# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError

from compass_visits.dao.compass import Compass
from compass_visits.dao.pws import get_netid_by_syskey
from compass_visits.dao.visit_dao import map_visit_to_compass_model
from compass_visits.models import Visit


class Command(BaseCommand):
    """
    Sync completed local visits to Compass and delete local rows on success.

    Intended to run periodically (e.g. cron). Rows that fail to sync are
    retained for retry in a subsequent run.
    """

    help = "Sync completed visits to Compass and delete synced local rows"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Maximum number of completed visits to process",
        )

    def handle(self, *args, **options):
        limit = options.get("limit")

        visits_qs = (Visit.objects.select_related(
            "program_area", "tutoring_option", "writing_service"
        )
            .filter(is_verified=True, check_out_date__isnull=False)
            .order_by("id"))

        if limit is not None:
            visits_qs = visits_qs[:limit]

        total = 0
        synced = 0
        failed = 0

        compass = Compass()

        for visit in visits_qs:
            total += 1
            try:
                student_netid = get_netid_by_syskey(visit.student_syskey)
                compass_visit = map_visit_to_compass_model(visit,
                                                           student_netid)
                compass.store_visit(compass_visit)
                visit.delete()
                synced += 1
            except Exception as ex:
                failed += 1
                self.stderr.write(
                    f"Failed visit id={visit.id} syskey={visit.student_syskey}:"
                    f" {ex}"
                )

        self.stdout.write(
            f"Processed={total} Synced={synced} Deleted={synced} Failed={failed}"
        )

        if failed:
            raise CommandError(f"Failed to sync {failed} visit(s)")
