from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, permissions, serializers,  filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import FieldActivity
from .serializers import FieldActivitySerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # ফ্রন্টএন্ড থেকে ?page_size=20 পাঠালে কাজ করবে
    max_page_size = 100


class FieldActivityViewSet(viewsets.ModelViewSet):
    queryset = FieldActivity.objects.select_related('user', 'division', 'district', 'upazila').all()
    serializer_class = FieldActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination  # 👈 Custom Pagination যুক্ত করা হলো
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'division', 'district', 'upazila', 'date']
    search_fields = ['visit_area', 'purpose_of_visit', 'contact_person']
    ordering_fields = ['date', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        # ১. সাধারণ ইউজারদের জন্য এডিট রেস্ট্রিকশন
        if not (user.is_staff or user.is_superuser):
            # নিজের তৈরি করা না হলে এডিট ব্লক
            if instance.user != user:
                raise serializers.ValidationError({"detail": "আপনি এই ডাটা এডিট করার অনুমতি রাখেন না।"})
            
            # SUBMITTED/APPROVED/REJECTED হলে এডিট করতে পারবে না (শুধুমাত্র DRAFT অবস্থায় পারবে)
            if instance.status != 'DRAFT':
                raise serializers.ValidationError({"detail": "শুধুমাত্র ড্রাফট (DRAFT) অবস্থায় এডিট করা সম্ভব।"})

            # সাধারণ ইউজার এডমিন রিমার্কস ও স্ট্যাটাস APPROVED/REJECTED করতে পারবে না
            serializer.save(
                status=serializer.validated_data.get('status', instance.status),
                remarks=instance.remarks # Remarks পরিবর্তন প্রতিরোধ
            )
        else:
            # ২. Admin / Superadmin-দের জন্য পূর্ণ এডিট সুবিধা
            serializer.save()