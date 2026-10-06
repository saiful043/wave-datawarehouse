from celery import shared_task
from .services import BeneficiaryETLService

@shared_task(bind=True)
def process_large_beneficiary_excel_task(self, file_path, project_id,package_id, batch_size=5000):
    """
    Celery task invoking ETL Service
    """
    service = BeneficiaryETLService(
        file_path=file_path, 
        project_id=project_id, 
        package_id=package_id, 
        batch_size=batch_size, 
        celery_task=self
    )
    return service.run()