from rest_framework import serializers
from .models import EarnParentTask, EarnTaskTemplate, EarnTaskSubmission

class EarnParentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EarnParentTask
        fields = '__all__'

class EarnTaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EarnTaskTemplate
        fields = '__all__'


class EarnTaskSubmissionSerializer(serializers.ModelSerializer):
    task_template_detail = EarnTaskTemplateSerializer(source='task_template', read_only=True)
    upazila_name = serializers.CharField(source='upazila.name_en', read_only=True)
    district_name = serializers.CharField(source='district.name_en', read_only=True)
    division_name = serializers.CharField(source='division.name_en', read_only=True)
    submitted_by_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = EarnTaskSubmission
        fields = '__all__'
        # 🟢 এই ৩টি ফিল্ডকে read_only বানাতে হবে যেন রিকোয়েস্টে না পাঠালেও validation error না দেয়
        extra_kwargs = {
            'division': {'required': False, 'allow_null': True},
            'district': {'required': False, 'allow_null': True},
            'upazila': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            validated_data['user'] = user

            # 🟢 User profile (http://localhost:8000/api/auth/me/) থেকে auto location fetch
            if hasattr(user, 'profile'):
                profile = user.profile
                if profile.division:
                    validated_data['division'] = profile.division
                if profile.district:
                    validated_data['district'] = profile.district
                if profile.upazila:
                    validated_data['upazila'] = profile.upazila

        return super().create(validated_data)