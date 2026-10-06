from django.urls import path
from .views import BeneficiaryImportAPIView, TaskStatusAPIView

urlpatterns = [
    path('import/beneficiary/', BeneficiaryImportAPIView.as_view(), name='beneficiary-import'),
    path('import/status/<str:task_id>/', TaskStatusAPIView.as_view(), name='import-status'),
]