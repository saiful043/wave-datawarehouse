from rest_framework import serializers
from .models import Project
from apps.programs.serializers import ProgramSerializer

class ProjectSerializer(serializers.ModelSerializer):
    program_detail = ProgramSerializer(source='program', read_only=True)
    class Meta:
        model = Project
        fields = [
            'id', 
            'program',  # 👈 রাইট/ক্রিয়েট করার সময় Program ID দিতে হবে (Required)
            'program_detail',
            'code', 
            'title', 
            'donor', 
            'description', 
            'duration', 
            'location', 
            'target_beneficiaries', 
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']