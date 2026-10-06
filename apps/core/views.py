from rest_framework import viewsets, permissions
from apps.core.models import Gender
from apps.core.serializers import GenderSerializer

class GenderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gender.objects.filter(status=1).order_by('display_order')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GenderSerializer