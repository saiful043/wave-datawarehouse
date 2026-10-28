from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper
from .models import EarnParentTask, EarnTaskTemplate, EarnTaskSubmission
from .serializers import EarnParentTaskSerializer, EarnTaskTemplateSerializer, EarnTaskSubmissionSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EarnParentTaskViewSet(viewsets.ModelViewSet):
    queryset = EarnParentTask.objects.all().order_by('id')
    serializer_class = EarnParentTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    filterset_fields = ['task_id']
    search_fields = ['name', 'task_id']

class EarnTaskTemplateViewSet(viewsets.ModelViewSet):
    queryset = EarnTaskTemplate.objects.all().order_by('id')
    serializer_class = EarnTaskTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = None
    
    filterset_fields = ['parent_task', 'level', 'task_code']
    search_fields = ['task_name', 'task_code']


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

        # 4. Status Breakdown (Submission status)
        status_breakdown = list(
            submissions.values('status').annotate(task_count=Count('id'))
        )

        # 📊 Screen-shot Wise: Parent Task (Deliverable) Progress Summary
        # প্রতিটি Parent Task এর আন্ডারে থাকা টেমপ্লেট এবং সাবমিশন স্ট্যাটাস কাউন্ট করা
        parent_tasks = EarnParentTask.objects.all()
        deliverable_progress = []

        for pt in parent_tasks:
            # এই Parent Task এর আন্ডারে কয়টি EarnTaskTemplate আছে (Total Acts)
            total_acts = EarnTaskTemplate.objects.filter(parent_task=pt).count()

            # এই Parent Task এর সাবমিশনগুলোর ওপর ফিল্টার
            pt_submissions = submissions.filter(task_template__parent_task=pt)

            completed_count = pt_submissions.filter(status='Completed').count()
            in_progress_count = pt_submissions.filter(status='In Progress').count()
            delayed_count = pt_submissions.filter(status='Delayed').count()
            not_started_count = pt_submissions.filter(status='Not Started').count()

            # Complete % হিসাব (Completed / Total Acts * 100)
            completion_percentage = (completed_count / total_acts * 100) if total_acts > 0 else 0.0

            deliverable_progress.append({
                'task_id': pt.task_id,            # যেমন: D1, D2
                'name': pt.name,                  # যেমন: Project Mobilization...
                'total_acts': total_acts,
                'completed': completed_count,
                'in_progress': in_progress_count,
                'delayed': delayed_count,
                'not_started': not_started_count,
                'completion_percentage': round(completion_percentage, 2)
            })


            # 📅 Biannual Progress Calculation
            BIANNUAL_PERIODS = [
                {'period': 'H1', 'name_en': 'Jul–Dec 2026', 'start': '2026-07-01', 'end': '2026-12-31'},
                {'period': 'H2', 'name_en': 'Jan–Jun 2027', 'start': '2027-01-01', 'end': '2027-06-30'},
                {'period': 'H3', 'name_en': 'Jul–Dec 2027', 'start': '2027-07-01', 'end': '2027-12-31'},
                {'period': 'H4', 'name_en': 'Jan–Jun 2028', 'start': '2028-01-01', 'end': '2028-06-30'},
                {'period': 'H5', 'name_en': 'Jul–Dec 2028', 'start': '2028-07-01', 'end': '2028-12-31'},
            ]

            biannual_progress = []
            for p in BIANNUAL_PERIODS:
                period_templates = EarnTaskTemplate.objects.filter(
                    planned_period_from__lte=p['end'],
                    planned_period_to__gte=p['start']
                )
                total_acts = period_templates.count()
                p_submissions = submissions.filter(task_template__in=period_templates)

                completed_count = p_submissions.filter(status='Completed').count()
                in_progress_count = p_submissions.filter(status='In Progress').count()
                delayed_count = p_submissions.filter(status='Delayed').count()
                not_started_count = p_submissions.filter(status='Not Started').count()
                completion_percentage = (completed_count / total_acts * 100) if total_acts > 0 else 0.0

                biannual_progress.append({
                    'period': p['period'],
                    'date_range': p['name_en'],
                    'total_acts': total_acts,
                    'completed': completed_count,
                    'in_progress': in_progress_count,
                    'delayed': delayed_count,
                    'not_started': not_started_count,
                    'completion_percentage': round(completion_percentage, 2)
                })

            # 📝 Daily Log Summary
            total_log_entries = submissions.count()
            latest_submission = submissions.order_by('-submitted_at').first()
            latest_entry_date = latest_submission.submitted_at.strftime('%d-%b-%Y') if latest_submission and latest_submission.submitted_at else '-'

            daily_log_summary = {
                'total_log_entries': total_log_entries,
                'latest_entry_date': latest_entry_date
            }

        return Response({
            'total_templates': total_templates,
            'status_breakdown': status_breakdown,
            'target_upazila_summary': target_upazila_summary,
            'deliverable_progress': deliverable_progress,
            'biannual_progress': biannual_progress,
            'daily_log_summary': daily_log_summary,
            
        })