from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """
    Projects Full CRUD API (Create, Read, Update, Delete)
    """
    queryset = Project.objects.all().order_by('-created_at') if hasattr(Project, 'created_at') else Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]