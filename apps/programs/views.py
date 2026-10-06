from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters, permissions
from .models import Program
from .serializers import ProgramSerializer

class ProgramViewSet(viewsets.ModelViewSet):
    """
    Program Model-এর জন্য CRUD (Create, Read, Update, Delete) ViewSet
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    
    # সার্চ ও সর্টিং সুবিধার জন্য
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering = ['code']
    permission_classes = [permissions.IsAuthenticated]  # শুধুমাত্র লগইন করা ব্যবহারকারীরাই অ্যাক্সেস করতে পারবে