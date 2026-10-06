from django.core.management.base import BaseCommand
from apps.etl_engine.services import LookupETLManager


class Command(BaseCommand):
    help = "Sync all API lookups into Data Warehouse DB"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("--- Starting All Lookup Syncs ---"))

        # Location sync
        self.stdout.write("Syncing Locations...")
        success = LookupETLManager.sync_locations()

        if success:
            self.stdout.write(self.style.SUCCESS("--- Location Sync Completed Successfully ---"))
        else:
            self.stdout.write(self.style.ERROR("--- Location Sync Failed ---"))