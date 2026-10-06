from rest_framework import serializers
from .models import Program

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'id', 
            'code', 
            'name', 
            'description', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        """
        Code ফিল্ডটিকে সবসময় uppercase (বড় হাতের অক্ষরে) কনভার্ট করার জন্য
        """
        return value.upper().strip()