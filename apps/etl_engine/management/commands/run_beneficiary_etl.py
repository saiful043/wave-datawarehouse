from django.core.management.base import BaseCommand
from apps.etl_engine.services import BeneficiaryETLService

class Command(BaseCommand):
    help = 'Run ETL Beneficiary import pipeline'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to Excel/CSV file')
        parser.add_argument('--project_id', type=int, required=True, help='Target Project ID')

    def handle(self, *args, **options):
        service = BeneficiaryETLService(options['file_path'], options['project_id'])
        result = service.run()
        
        self.stdout.write(self.style.SUCCESS(f"ETL Execution Complete. Success: {result['success_count']}"))
        if result['errors']:
            self.stdout.write(self.style.WARNING(f"Errors encountered: {len(result['errors'])}"))