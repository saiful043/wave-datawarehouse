from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult

from .tasks import process_large_beneficiary_excel_task


class BeneficiaryImportAPIView(APIView):
    """
    ফাইল আপলোড করে ব্যাকগ্রাউন্ডে ETL প্রসেস শুরু করার API
    """
    def post(self, request):
        file_obj = request.FILES.get('file')
        project_id = request.data.get('project_id')
        package_id = request.data.get('package_id')

        if not file_obj or not project_id or not package_id:
            return Response(
                {"error": "File and project_id and package_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ১. ফাইলটি সাময়িকভাবে সার্ভারে সেভ করা
        file_name = f"temp_imports/{file_obj.name}"
        saved_path = default_storage.save(file_name, file_obj)
        full_path = default_storage.path(saved_path)

        # ২. Celery Task ব্যাকগ্রাউন্ডে চালানো
        # task = process_large_beneficiary_excel_task.delay(full_path, int(project_id))
        task = process_large_beneficiary_excel_task.delay(full_path, project_id, package_id)

        return Response({
            "message": "Import task initiated successfully.",
            "task_id": task.id
        }, status=status.HTTP_202_ACCEPTED)


class TaskStatusAPIView(APIView):
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        
        if task_result.state == 'PENDING':
            response = {'status': 'PENDING', 'progress': {'processed': 0, 'total': 100}}
        elif task_result.state == 'PROGRESS':
            response = {
                'status': 'PROGRESS',
                'progress': task_result.info # {'processed': 10, 'total': 10}
            }
        elif task_result.state == 'SUCCESS':
            response = {
                'status': 'SUCCESS', # 👈 ফ্রন্টএন্ড এই 'SUCCESS' স্ট্যাটাস খুঁজছে
                'result': task_result.result
            }
        else: # FAILURE / REVOKED
            response = {
                'status': task_result.state,
                'error': str(task_result.info)
            }
            
        return Response(response)