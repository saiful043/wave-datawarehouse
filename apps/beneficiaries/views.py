from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.views import APIView
from django.db.models import Count, Q
from .models import BeneficiaryDifficulty
from .models import BeneficiaryInfo
from apps.beneficiaries.models import BeneficiaryEducationInfo
from apps.core.constants import HIGHEST_EDUCATION_LEVEL_CONFIG
from .models import BeneficiaryHouseHoldInfo


from .models import BeneficiaryInfo
from .serializers import (
    BeneficiarySerializer,
    BeneficiaryDetailSerializer,
    BeneficiaryWriteSerializer
)

# Core constants import
from apps.core import constants as core_constants
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BeneficiaryViewSet(viewsets.ModelViewSet):
    """
    Unified ViewSet for Beneficiary CRUD and detail profile fetching.
    Optimized to prevent N+1 queries using exact related names.
    """
    pagination_class = StandardResultsSetPagination
    queryset = BeneficiaryInfo.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['applicant_gender', 'status', 'geo_location__district_id']
    search_fields = ['response_id', 'applicant_name_en', 'applicant_name_bn', 'mobile_self', 'applicant_nid']
    ordering_fields = ['id', 'created_at', 'applicant_name_en']
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list':
            return queryset.select_related(
                'applicant_gender',
                'geo_location__district',
                'geo_location__upazila',
                'geo_location__union'
            )
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return queryset.select_related(
                'applicant_gender',
                'geo_location',
                'household_info',
                'difficulty_profile',
                'edu_info',
                'employment_info',
                'digital_skill',
                'willingness_info'
            )

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return BeneficiarySerializer
        elif self.action == 'retrieve':
            return BeneficiaryDetailSerializer
        return BeneficiaryWriteSerializer

    @action(detail=False, methods=['get'], url_path='form-config')
    def get_form_config(self, request):
        """
        Endpoint to serve dynamic form choice configs for Frontend UI.
        """
        config_data = {
            'relation_to_hh_head': getattr(core_constants, 'RELATION_TO_HH_HEAD_CONFIG', None),
            'marital_status': getattr(core_constants, 'MARITAL_STATUS_CONFIG', None),
            'special_area': getattr(core_constants, 'HOUSEHOLE_SPECIAL_AREA_CONFIG', None),
            'hh_uncollected_reason': getattr(core_constants, 'HH_COUNT_UNCOLLECTED_REASON_CONFIG', None),
        }
        return Response(config_data, status=status.HTTP_200_OK)


class DisabilityChartDataView(APIView):
    def get(self, request, *args, **kwargs):
        # বাংলা নামসহ ফিল্ড ম্যাপিং
        category_map = {
            'walking': 'চলাফেরা',
            'seeing': 'দৃষ্টি',
            'hearing': 'শ্রবণ',
            'remembering': 'স্মৃতিশক্তি/মনোযোগ',
            'selfcare': 'নিজের যত্ন',
            'communicating': 'যোগাযোগ'
        }

        # প্রতিটি ক্যাটাগরিতে অন্তত কিছুটা সমস্যা (181, 182, 183) থাকা বেনিফিশিয়ারি সংখ্যা গননা
        aggregations = {}
        for cat in category_map.keys():
            aggregations[cat] = Count('pk', filter=Q(**{f"{cat}__in": [181, 182, 183]}))

        stats = BeneficiaryDifficulty.objects.aggregate(**aggregations)

        # আউটপুট প্রস্তুত করা
        summary_data = [
            {
                "category_en": cat,
                "label": category_map[cat],
                "count": stats[cat],
                "display_text": f"{category_map[cat]} {stats[cat]} জন"
            }
            for cat in category_map.keys()
        ]

        return Response({
            "summary": summary_data
        })

class GenderChartDataView(APIView):
    def get(self, request, *args, **kwargs):
        # applicant_gender_id অনুযায়ী কাউন্ট বের করা
        gender_counts = (
            BeneficiaryInfo.objects.values('applicant_gender_id')
            .annotate(count=Count('id'))
            .order_by('applicant_gender_id')
        )

        summary = []
        for item in gender_counts:
            g_id = item['applicant_gender_id']
            
            # ID অনুযায়ী বাংলা লেবেল নির্ধারণ
            if g_id == 1:
                label = "পুরুষ"
            elif g_id == 2:
                label = "নারী"
            elif g_id == 3:
                label = "তৃতীয় লিঙ্গ"
            else:
                label = "অন্যান্য"

            if g_id is not None:
                summary.append({
                    "gender_id": g_id,
                    "label": label,
                    "count": item['count']
                })

        return Response({"summary": summary}, status=status.HTTP_200_OK)

class EducationChartDataView(APIView):
    def get(self, request, *args, **kwargs):
        # Database irraa galmeewwan barumsaa lakkaawuu
        edu_counts = (
            BeneficiaryEducationInfo.objects.values('highest_education_level')
            .annotate(count=Count('beneficiary_id'))
            .order_by('highest_education_level')
        )
        
        # Dictionary kaayyoo lakkoofsa safaruu
        counts_dict = {item['highest_education_level']: item['count'] for item in edu_counts}
        
        options = HIGHEST_EDUCATION_LEVEL_CONFIG.get('options', [])
        # displayOrder irratti hundaa'uun tartiibeessuu
        sorted_options = sorted(options, key=lambda x: x.get('displayOrder', 0))
        
        total_count = sum(counts_dict.values())
        
        summary = []
        running_count = 0
        
        for opt in sorted_options:
            val = int(opt['value'])
            count = counts_dict.get(val, 0)
            running_count += count
            
            # Cumulative percentage (pct cum) yaada lakkaa'a
            cumulative_percentage = round((running_count / total_count * 100), 1) if total_count > 0 else 0
            
            summary.append({
                "level_id": val,
                "label_bn": opt['labelBn'],
                "label_en": opt['labelEn'],
                "count": count,
                "cumulative": cumulative_percentage
            })
            
        return Response({
            "total": total_count,
            "summary": summary
        }, status=status.HTTP_200_OK)

class AgePyramidChartDataView(APIView):
    def get(self, request, *args, **kwargs):
        # বয়সের গ্রুপসমূহ নির্ধারণ
        age_ranges = [
            {"group": "১৫-২০ বছর", "min_age": 15, "max_age": 20},
            {"group": "২১-২৫ বছর", "min_age": 21, "max_age": 25},
            {"group": "২৬-৩০ বছর", "min_age": 26, "max_age": 30},
            {"group": "৩১-৩৫ বছর", "min_age": 31, "max_age": 35},
            {"group": "৩৬-৪০ বছর", "min_age": 36, "max_age": 40},
            {"group": "৪১+ বছর", "min_age": 41, "max_age": 120},
        ]

        summary = []
        
        # প্রতিটি বয়স গ্রুপের জন্য পুরুষ (id=1) এবং নারী (id=2) গণনা
        for r in age_ranges:
            m_count = BeneficiaryInfo.objects.filter(
                applicant_age__gte=r["min_age"],
                applicant_age__lte=r["max_age"],
                applicant_gender_id=1
            ).count()

            f_count = BeneficiaryInfo.objects.filter(
                applicant_age__gte=r["min_age"],
                applicant_age__lte=r["max_age"],
                applicant_gender_id=2
            ).count()

            summary.append({
                "group": r["group"],
                "male": m_count,
                "female": f_count
            })

        return Response({"summary": summary}, status=status.HTTP_200_OK)

class EthnicChartDataView(APIView):
    def get(self, request, *args, **kwargs):
        # ক্ষুদ্র নৃগোষ্ঠী হিসেবে চিহ্নিত (is_indigenous=True) পরিবারগুলোর গ্রুপ অনুসারে সংখ্যা
        ethnic_counts = (
            BeneficiaryHouseHoldInfo.objects.filter(is_indigenous=True)
            .values(
                'indigenous_group_type_id',
                'indigenous_group_type__label_bn', # আপনার core.IndigenousGroupType মডেলে নাম অনুযায়ী পরিবর্তন করতে পারেন
                'indigenous_group_type__label_en'
            )
            .annotate(count=Count('beneficiary_id'))
            .order_by('-count')
        )

        summary = []
        # বারের কালার সাইকেলের জন্য কিছু হেক্স কালার কোড
        colors = ["#3B6A8C", "#A25247", "#B8822B", "#2E7D32", "#6A1B9A", "#D84315"]

        for idx, item in enumerate(ethnic_counts):
            group_name = item['indigenous_group_type__label_bn'] or item['indigenous_group_type__label_en'] or "অন্যান্য"
            summary.append({
                "group_id": item['indigenous_group_type_id'],
                "group": group_name,
                "count": item['count'],
                "color": colors[idx % len(colors)]
            })

        return Response({"summary": summary}, status=status.HTTP_200_OK)