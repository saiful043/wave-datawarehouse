from rest_framework import status, viewsets, permissions
#user start
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, GroupSerializer, ChangePasswordSerializer
#user end

from django_filters import rest_framework as filters
from apps.core.models import Location
from apps.core.serializers import LocationSerializer

from apps.core.models import Package
from apps.core.serializers import PackageSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from apps.core.constants import HH_COUNT_UNCOLLECTED_REASON_CONFIG


from apps.projects.models import Project  
from apps.projects.serializers import ProjectSerializer

#user
# UserViewSet আপডেট করুন
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related(
        'profile__gender', 
        'profile__division', 
        'profile__district', 
        'profile__upazila', 
        'profile__union', 
        'profile__village'
    ).order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# Current Logged-in User Profile
@api_view(['GET', 'PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method in ['PATCH', 'PUT']:
        # Nested profile data handling
        data = request.data.dict() if hasattr(request.data, 'dict') else request.data.copy()
        
        # Multipart form-data te nested object pathale setup:
        profile_data = {}
        if 'mobile_no' in data:
            profile_data['mobile_no'] = data.pop('mobile_no')
        if 'profile_pic' in request.FILES:
            profile_data['profile_pic'] = request.FILES['profile_pic']

        if profile_data:
            data['profile'] = profile_data

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Change Password View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if not user.check_password(old_password):
        return Response({"error": "Puraon password ti sothik noy."}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({"message": "Password safollobhabe poribortito hoyeche."})

# Superadmin Viewsets for Users & Groups
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # Superadmin / Staff shudhu access pabe

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
#user end


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ফ্রন্টএন্ডের ড্রপডাউনে দেখানোর জন্য প্রজেক্ট লিস্ট পাঠাবে।
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class LocationFilter(filters.FilterSet):
    class Meta:
        model = Location
        fields = {
            'type': ['exact'],
            'parent_location_id': ['exact'],
        }


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API — শুধু listing/detail দরকার, insert/update
    হবে management command দিয়ে (আগের import_locations command)।
    """
    queryset = Location.objects.all().order_by('name_en')
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = LocationFilter
    search_fields = ['name_en', 'name_bn', 'code']

class LocationStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        by_type = (
            Location.objects.values('type')
            .annotate(count=Count('location_id'))
            .order_by('type')
        )
        return Response({
            'total': Location.objects.count(),
            'by_type': list(by_type),
        })

class ReasonNotCollectedViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]  # 👈 সুরক্ষিত রাখার জন্য IsAuthenticated

    def list(self, request):
        return Response(HH_COUNT_UNCOLLECTED_REASON_CONFIG)

class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Frontend user boundary: Read-only access for listing and viewing package details.
    """
    queryset = Package.objects.all().order_by('sort_order', 'id')
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated]  # আপনার প্রেফারেন্স অনুযায়ী পারমিশন সামঞ্জস্য করুন