from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from .models import EarnTaskTemplate, EarnTaskSubmission
from .serializers import EarnTaskTemplateSerializer, EarnTaskSubmissionSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EarnTaskTemplateViewSet(viewsets.ModelViewSet):
    queryset = EarnTaskTemplate.objects.all().order_by('-id')
    serializer_class = EarnTaskTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['segment']
    search_fields = ['task_name', 'output']


class EarnTaskSubmissionViewSet(viewsets.ModelViewSet):
    queryset = EarnTaskSubmission.objects.all().select_related(
        'task_template', 'division', 'district', 'upazila', 'user'
    ).order_by('-submitted_at')
    serializer_class = EarnTaskSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filterset_fields = ['task_template', 'status', 'division', 'district', 'upazila']

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        if user.is_staff or user.is_superuser:
            return qs

        if hasattr(user, 'profile') and user.profile.upazila:
            return qs.filter(upazila=user.profile.upazila)

        return qs

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        user = request.user
        division_id = request.query_params.get('division')
        district_id = request.query_params.get('district')
        upazila_id = request.query_params.get('upazila')

        # 🎯 Selected Target Upazilas List
        TARGET_UPAZILAS = [387, 503, 383, 505, 705, 501, 502, 504, 704, 586, 578, 580, 584, 583, 581, 253, 248, 260, 249, 203]

        # Location filtering calculation
        submissions = EarnTaskSubmission.objects.all()

        # Upazila Manager Access Restriction: Auto filter to user's upazila
        if not (user.is_staff or user.is_superuser):
            if hasattr(user, 'profile') and user.profile.upazila:
                submissions = submissions.filter(upazila=user.profile.upazila)
        else:
            # Admin Location Filters
            if division_id:
                submissions = submissions.filter(division_id=division_id)
            if district_id:
                submissions = submissions.filter(district_id=district_id)
            if upazila_id:
                submissions = submissions.filter(upazila_id=upazila_id)

        # 🟢 Specific Target Upazilas Summary (Done, Due Soon, Ongoing)
        target_upazila_summary = list(
            submissions.filter(upazila_id__in=TARGET_UPAZILAS)
            .values('upazila__name_en', 'upazila__name_bn', 'status')
            .annotate(task_count=Count('id'))
        )

        # 1. Total Tasks Calculation
        total_templates = EarnTaskTemplate.objects.count()

        # 2. Tasks Per Segment
        segment_counts = list(
            EarnTaskTemplate.objects.values('segment').annotate(task_count=Count('id'))
        )

        # 3. Role-wise Workload Breakdown
        role_workload = {
            'UM': {
                'Lead': EarnTaskTemplate.objects.filter(um_role='Lead').count(),
                'Key Support': EarnTaskTemplate.objects.filter(um_role='Key Support').count(),
                'Support': EarnTaskTemplate.objects.filter(um_role='Support').count(),
            },
            'JPO': {
                'Lead': EarnTaskTemplate.objects.filter(jpo_role='Lead').count(),
                'Key Support': EarnTaskTemplate.objects.filter(jpo_role='Key Support').count(),
                'Support': EarnTaskTemplate.objects.filter(jpo_role='Support').count(),
            },
            'EDO': {
                'Lead': EarnTaskTemplate.objects.filter(edo_role='Lead').count(),
                'Key Support': EarnTaskTemplate.objects.filter(edo_role='Key Support').count(),
                'Support': EarnTaskTemplate.objects.filter(edo_role='Support').count(),
            }
        }

        # 4. Status Breakdown (Submission status)
        status_breakdown = list(
            submissions.values('status').annotate(task_count=Count('id'))
        )

        # 5. Segment-wise Status Summary
        segment_status_summary = list(
            submissions.values('task_template__segment', 'status')
            .annotate(count=Count('id'))
        )

        return Response({
            'total_templates': total_templates,
            'tasks_per_segment': segment_counts,
            'role_workload': role_workload,
            'status_breakdown': status_breakdown,
            'segment_status_summary': segment_status_summary,
            'target_upazila_summary': target_upazila_summary,
        })