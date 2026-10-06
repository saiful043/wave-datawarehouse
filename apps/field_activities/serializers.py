from rest_framework import serializers
from .models import FieldActivity
from apps.core.models import Location


class LocationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'name_en', 'name_bn', 'type']


class FieldActivitySerializer(serializers.ModelSerializer):
    # READ-ONLY FIELDS FOR FRONTEND DISPLAY
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    division_detail = LocationNestedSerializer(source='division', read_only=True)
    district_detail = LocationNestedSerializer(source='district', read_only=True)
    upazila_detail = LocationNestedSerializer(source='upazila', read_only=True)

    class Meta:
        model = FieldActivity
        fields = [
            'id',
            'user',
            'user_name',
            'user_username',
            'date',
            'division',
            'district',
            'upazila',
            'division_detail',
            'district_detail',
            'upazila_detail',
            'visit_area',
            'latitude',
            'longitude',
            'purpose_of_visit',
            'target_group',
            'contact_person',
            'number_of_meeting',
            'total_person_conducted',
            'meeting_details',
            'others',
            'meeting_photo',
            'remarks',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Auto assign logged-in user if not passed
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)