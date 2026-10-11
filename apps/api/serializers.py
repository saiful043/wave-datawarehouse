from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User, Group, Permission
from .models import UserProfile
from apps.core.models import Location, Gender

# Location Serializer (Nested data দেখানোর জন্য)
class LocationSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'name_en', 'name_bn', 'type']

# Gender Serializer
class GenderSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'label_en', 'label_bn']

# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    # ID দিয়ে পোস্ট করার জন্য PrimaryKeyRelatedField
    gender_id = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.all(), source='gender', write_only=True, required=False, allow_null=True
    )
    division_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='division', write_only=True, required=False, allow_null=True
    )
    district_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='district', write_only=True, required=False, allow_null=True
    )
    upazila_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='upazila', write_only=True, required=False, allow_null=True
    )
    union_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='union', write_only=True, required=False, allow_null=True
    )
    village_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='village', write_only=True, required=False, allow_null=True
    )

    # GET রিকোয়েস্টে বিস্তারিত ডাটা পাঠানোর জন্য Read-only fields
    gender = GenderSimpleSerializer(read_only=True)
    division = LocationSimpleSerializer(read_only=True)
    district = LocationSimpleSerializer(read_only=True)
    upazila = LocationSimpleSerializer(read_only=True)
    union = LocationSimpleSerializer(read_only=True)
    village = LocationSimpleSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'mobile_no', 'profile_pic', 
            'gender', 'gender_id',
            'division', 'division_id',
            'district', 'district_id',
            'upazila', 'upazila_id',
            'union', 'union_id',
            'village', 'village_id'
        ]

# 1. Permission Serializer
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']
        

class GroupSerializer(serializers.ModelSerializer):
    permissions_details = PermissionSerializer(source='permissions', many=True, read_only=True)
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        many=True,
        required=False
    )
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'permissions_details']


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="এই ইমেইল এড্রেস টি দিয়ে আগেই একটি একাউন্ট তৈরী করা আছে.")]
    )
    profile = UserProfileSerializer(required=False)

    # GET এ গ্রুপের ডিটেইলস এবং POST/PUT এ Group ID গ্রহণ করার জন্য
    groups_details = GroupSerializer(source='groups', many=True, read_only=True)
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'groups', 'groups_details', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        groups = validated_data.pop('groups', [])
        
        default_password = "ChangeMe@123"
        user = User.objects.create_user(**validated_data)
        user.set_password(default_password)
        user.save()

        # Profile তৈরি করা
        UserProfile.objects.create(user=user, **profile_data)

        if groups:
            user.groups.set(groups)

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        groups = validated_data.pop('groups', None)

        # Basic User fields update
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Profile update or create
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        if groups is not None:
            instance.groups.set(groups)

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)