from django.urls import path
from rest_framework.routers import DefaultRouter
#user
from .views import me_view, change_password_view, UserViewSet, GroupViewSet

from apps.api.views import (
    LocationViewSet, 
    LocationStatsView, 
    ReasonNotCollectedViewSet,
    PackageViewSet
)
from apps.core.views import GenderViewSet
from apps.projects.views import ProjectViewSet
from apps.programs.views import ProgramViewSet
from apps.beneficiaries.views import BeneficiaryViewSet  # Updated ViewSet Import
from apps.field_activities.views import FieldActivityViewSet
from apps.etl_engine.views import BeneficiaryImportAPIView, TaskStatusAPIView
from apps.beneficiaries.views import DisabilityChartDataView
from apps.beneficiaries.views import GenderChartDataView
from apps.beneficiaries.views import EducationChartDataView
from apps.beneficiaries.views import AgePyramidChartDataView
from apps.beneficiaries.views import EthnicChartDataView

router = DefaultRouter()
#user
router.register(r'users', UserViewSet, basename='users')
router.register(r'groups', GroupViewSet, basename='groups')


router.register(r'locations', LocationViewSet, basename='location')
router.register(r'core/genders', GenderViewSet, basename='gender')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'programs', ProgramViewSet, basename='program')
router.register(r'core/reasons-not-collected', ReasonNotCollectedViewSet, basename='reasons-not-collected')
router.register(r'beneficiaries', BeneficiaryViewSet, basename='beneficiary')  # Registered in Router

router.register(r'core/packages', PackageViewSet, basename='package')
router.register(r'field-activities', FieldActivityViewSet, basename='field-activity')

urlpatterns = [
    #user
    path('auth/me/', me_view, name='auth_me'),
    path('auth/change-password/', change_password_view, name='change_password'),
    #end
    path('locations/stats/', LocationStatsView.as_view(), name='location-stats'),
    path('etl/import-beneficiaries/', BeneficiaryImportAPIView.as_view(), name='import-beneficiaries'),
    # Task Status Check এর জন্য নিচের রাউটটি যুক্ত করা হলো:
    path('etl/task-status/<str:task_id>/', TaskStatusAPIView.as_view(), name='task-status'),
    path('beneficiaries/disability-chart/', DisabilityChartDataView.as_view(), name='disability-chart-data'),
    path('beneficiaries/gender-chart/', GenderChartDataView.as_view(), name='gender-chart-data'),
    path('beneficiaries/education-chart/', EducationChartDataView.as_view(), name='education-chart-data'),
    path('beneficiaries/age-chart/', AgePyramidChartDataView.as_view(), name='age-chart-data'),
    path('beneficiaries/ethnic-chart/', EthnicChartDataView.as_view(), name='ethnic-chart-data'),
] + router.urls