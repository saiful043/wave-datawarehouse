from rest_framework import serializers
from apps.core.models import Location
from apps.core.models import Gender
from apps.core.models import Package


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'location_id',
            'name_en',
            'name_bn',
            'parent_location_id',   # tomar model e field naam eta hole thik ache
            'type',
            'path_string',
            'code',
            'bbs_code',
            'bbs_code_path',
            'bbs_version_id',
        ]

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'label_en', 'label_bn', 'color_hex', 'display_order']

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            'id',
            'code',
            'name_en',
            'name_bn',
            'sort_order',
            'survey_target',
            'total_beneficiary_target',
            'created_at',
            'updated_at'
        ]