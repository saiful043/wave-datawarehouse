from rest_framework import serializers

# Core models from apps.core.models
from apps.core.models import Location, Gender, IndigenousGroupType,Package

# Beneficiaries models from current app
from .models import (
    BeneficiaryInfo,
    BeneficiaryGeoLocation,
    BeneficiaryHouseHoldInfo,
    BeneficiaryDifficulty,
    BeneficiaryEducationInfo,
    BeneficiaryEmploymentInfo,
    BeneficiaryDigitalSkill,
    BeneficiaryWillingnessInfo
)

from apps.core.constants import (MARITAL_STATUS_CONFIG, RELATION_TO_HH_HEAD_CONFIG,
 HH_COUNT_UNCOLLECTED_REASON_CONFIG,HOUSEHOLE_SPECIAL_AREA_CONFIG, RELATION_TO_HH_HEAD_CONFIG,
 DIFFICULTY_SEEING_CONFIG, DIFFICULTY_HEARING_CONFIG,DIFFICULTY_WALKING_CONFIG,
 DIFFICULTY_REMEMBERING_CONFIG, DIFFICULTY_SELFCARE_CONFIG, DIFFICULTY_COMMUNICATING_CONFIG,
 HIGHEST_EDUCATION_LEVEL_CONFIG,INSTITUTION_TYPE_CONFIG, MADRASHA_TYPE_CONFIG, DISCONTINUE_REASON_CONFIG,
 SELF_EMPLOYMENT_TYPE_CONFIG, WAGE_EMPLOYMENT_STATUS_CONFIG, REASON_FOR_LEAVING_WORK_CONFIG, 
 TRAINING_PROJECT_NAME_CONFIG, COMPUTER_SKILL_CONFIG, APP_USAGE_CONFIG, VEHICLE_TYPE_CONFIG, DRIVING_TRAINING_LOCATION_CONFIG,
 LIVELIHOOD_PLAN_CONFIG, EMPLOYMENT_CHALLENGE_TYPE_CONFIG, ONSITE_TRAINING_CHALLENGE_TYPE_CONFIG
)


# ==============================================================================
# 1. CORE / MASTER DATA SERIALIZERS
# ==============================================================================
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'


class IndigenousGroupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndigenousGroupType
        fields = '__all__'


# ==============================================================================
# 2. SUB-SECTION SERIALIZERS
# ==============================================================================

class BeneficiaryGeoLocationSerializer(serializers.ModelSerializer):
    # Foreign Key model থেকে নাম টেনে আনা
    division_name_en = serializers.CharField(source='division.name_en', read_only=True, default=None)
    division_name_bn = serializers.CharField(source='division.name_bn', read_only=True, default=None)
    
    district_name_en = serializers.CharField(source='district.name_en', read_only=True, default=None)
    district_name_bn = serializers.CharField(source='district.name_bn', read_only=True, default=None)
    
    upazila_name_en = serializers.CharField(source='upazila.name_en', read_only=True, default=None)
    upazila_name_bn = serializers.CharField(source='upazila.name_bn', read_only=True, default=None)

    union_name_en = serializers.CharField(source='union.name_en', read_only=True, default=None)
    union_name_bn = serializers.CharField(source='union.name_bn', read_only=True, default=None)

    ward_name_en = serializers.CharField(source='ward.name_en', read_only=True, default=None)
    ward_name_bn = serializers.CharField(source='ward.name_bn', read_only=True, default=None)

    village_name_en = serializers.CharField(source='village.name_en', read_only=True, default=None)
    village_name_bn = serializers.CharField(source='village.name_bn', read_only=True, default=None)

    pouroword_or_union = serializers.SerializerMethodField()

    class Meta:
        model = BeneficiaryGeoLocation
        fields = '__all__'
    
    def get_pouroword_or_union(self, obj):
        if obj.pouroword_or_union == 1:
            return "পৌরওয়ার্ড"
        elif obj.pouroword_or_union == 2:
            return "ইউনিয়ন"
        
        return None


class BeneficiaryHouseHoldInfoSerializer(serializers.ModelSerializer):
    hh_head_gender = GenderSerializer(read_only=True)
    hh_count_1535_uncollected_reason = serializers.SerializerMethodField()
    indigenous_group_type = IndigenousGroupTypeSerializer(read_only=True)
    household_special_area = serializers.SerializerMethodField()
    

    class Meta:
        model = BeneficiaryHouseHoldInfo
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # hh_head_gender থাকলে সেটাকে GenderSerializer দিয়ে অবজেক্ট আকারে পাঠাবে
        if instance.hh_head_gender:
            representation['hh_head_gender'] = GenderSerializer(instance.hh_head_gender).data
        return representation
    
    def get_hh_count_1535_uncollected_reason(self, obj):
        raw_val = obj.hh_count_1535_uncollected_reason
        if not raw_val:
            return []

        # ডাটাবেজে ডাটা string ("1,2,3") নাকি list ([1, 2, 3]) হিসেবে আছে তা হ্যান্ডেল করা
        if isinstance(raw_val, str):
            selected_values = [v.strip() for v in raw_val.split(',') if v.strip()]
        elif isinstance(raw_val, list):
            selected_values = [str(v) for v in raw_val]
        else:
            selected_values = [str(raw_val)]

        result = []
        options = HH_COUNT_UNCOLLECTED_REASON_CONFIG.get('options', [])

        # সেলেক্টেড ভ্যালুগুলোর সাথে ম্যাচ করে labelEn এবং labelBn সহ অবজেক্ট তৈরি করা
        for val in selected_values:
            for option in options:
                if str(option.get('value')) == val:
                    result.append({
                        "value": option.get('value'),
                        "labelEn": option.get('labelEn'),
                        "labelBn": option.get('labelBn')
                    })
                    break

        return result
    
    def get_household_special_area(self, obj):
        if not obj.household_special_area:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.household_special_area)
        
        # HOUSEHOLE_SPECIAL_AREA_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in HOUSEHOLE_SPECIAL_AREA_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None
   


class BeneficiaryDifficultySerializer(serializers.ModelSerializer):
    seeing = serializers.SerializerMethodField()
    hearing = serializers.SerializerMethodField()
    walking = serializers.SerializerMethodField()
    remembering = serializers.SerializerMethodField()
    selfcare = serializers.SerializerMethodField()
    communicating = serializers.SerializerMethodField()
    class Meta:
        model = BeneficiaryDifficulty
        fields = '__all__'
    
    def get_seeing(self, obj):
        if not obj.seeing:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.seeing)
        
        # DIFFICULTY_SEEING_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in DIFFICULTY_SEEING_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None
    
    def get_hearing(self, obj):
        if not obj.hearing:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.hearing)
        
        # DIFFICULTY_HEARING_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in DIFFICULTY_HEARING_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None
    
    def get_walking(self, obj):
        if not obj.walking:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.walking)
        
        # DIFFICULTY_WALKING_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in DIFFICULTY_WALKING_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None

    
    def get_remembering(self, obj):
        if not obj.remembering:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.remembering)
        
        # DIFFICULTY_REMEMBERING_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in DIFFICULTY_REMEMBERING_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None

    def get_selfcare(self, obj):
        if not obj.selfcare:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.selfcare)
        
        # DIFFICULTY_SELFCARE_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in DIFFICULTY_SELFCARE_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None

    def get_communicating(self, obj):
        if not obj.communicating:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.communicating)
        
        # DIFFICULTY_COMMUNICATING_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in DIFFICULTY_COMMUNICATING_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None


class BeneficiaryEducationInfoSerializer(serializers.ModelSerializer):
    highest_education_level = serializers.SerializerMethodField()
    institution_type  = serializers.SerializerMethodField()
    madrasha_type = serializers.SerializerMethodField()
    discontinue_reason = serializers.SerializerMethodField()
    class Meta:
        model = BeneficiaryEducationInfo
        fields = '__all__'

    def get_highest_education_level(self, obj):
        if not obj.highest_education_level:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.highest_education_level)
        
        # HIGHEST_EDUCATION_LEVEL_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in HIGHEST_EDUCATION_LEVEL_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None

    def get_institution_type(self, obj):
        if not obj.institution_type:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.institution_type)
        
        # INSTITUTION_TYPE_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in INSTITUTION_TYPE_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None
    
    def get_madrasha_type(self, obj):
        if not obj.madrasha_type:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.madrasha_type)
        
        # MADRASHA_TYPE_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in MADRASHA_TYPE_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None

    
    def get_discontinue_reason(self, obj):
        raw_val = obj.discontinue_reason
        if not raw_val:
            return []

        # ডাটাবেজে ডাটা string ("1,2,3") নাকি list ([1, 2, 3]) হিসেবে আছে তা হ্যান্ডেল করা
        if isinstance(raw_val, str):
            selected_values = [v.strip() for v in raw_val.split(',') if v.strip()]
        elif isinstance(raw_val, list):
            selected_values = [str(v) for v in raw_val]
        else:
            selected_values = [str(raw_val)]

        result = []
        options = DISCONTINUE_REASON_CONFIG.get('options', [])

        # সেলেক্টেড ভ্যালুগুলোর সাথে ম্যাচ করে labelEn এবং labelBn সহ অবজেক্ট তৈরি করা
        for val in selected_values:
            for option in options:
                if str(option.get('value')) == val:
                    result.append({
                        "value": option.get('value'),
                        "labelEn": option.get('labelEn'),
                        "labelBn": option.get('labelBn')
                    })
                    break

        return result


class BeneficiaryEmploymentInfoSerializer(serializers.ModelSerializer):
    current_employment_type = serializers.SerializerMethodField()
    wage_employment_status = serializers.SerializerMethodField()
    left_work_reason = serializers.SerializerMethodField()
    training_project_name = serializers.SerializerMethodField()

    class Meta:
        model = BeneficiaryEmploymentInfo
        fields = '__all__'
    
    def get_current_employment_type(self, obj):
        if not obj.current_employment_type:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.current_employment_type)
        
        # SELF_EMPLOYMENT_TYPE_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in SELF_EMPLOYMENT_TYPE_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None
    
    def get_wage_employment_status(self, obj):
        if not obj.wage_employment_status:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.wage_employment_status)
        
        # WAGE_EMPLOYMENT_STATUS_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in WAGE_EMPLOYMENT_STATUS_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None
    
    def get_left_work_reason(self, obj):
        if not obj.left_work_reason:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.left_work_reason)
        
        # REASON_FOR_LEAVING_WORK_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in REASON_FOR_LEAVING_WORK_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None 
    def get_training_project_name(self, obj):
        if not obj.training_project_name:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.training_project_name)
        
        # TRAINING_PROJECT_NAME_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in TRAINING_PROJECT_NAME_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None


class BeneficiaryDigitalSkillSerializer(serializers.ModelSerializer):
    computer_skill = serializers.SerializerMethodField()
    app_usage = serializers.SerializerMethodField()
    vehicle_type = serializers.SerializerMethodField()
    driving_training_location = serializers.SerializerMethodField()
    
    class Meta:
        model = BeneficiaryDigitalSkill
        fields = '__all__'
    
    def get_computer_skill(self, obj):
        if not obj.computer_skill:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.computer_skill)
        
        # COMPUTER_SKILL_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in COMPUTER_SKILL_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None
    
    def get_app_usage(self, obj):
        raw_val = obj.app_usage
        if not raw_val:
            return []

        # ডাটাবেজে ডাটা string ("1,2,3") নাকি list ([1, 2, 3]) হিসেবে আছে তা হ্যান্ডেল করা
        if isinstance(raw_val, str):
            selected_values = [v.strip() for v in raw_val.split(',') if v.strip()]
        elif isinstance(raw_val, list):
            selected_values = [str(v) for v in raw_val]
        else:
            selected_values = [str(raw_val)]

        result = []
        options = APP_USAGE_CONFIG.get('options', [])

        # সেলেক্টেড ভ্যালুগুলোর সাথে ম্যাচ করে labelEn এবং labelBn সহ অবজেক্ট তৈরি করা
        for val in selected_values:
            for option in options:
                if str(option.get('value')) == val:
                    result.append({
                        "value": option.get('value'),
                        "labelEn": option.get('labelEn'),
                        "labelBn": option.get('labelBn')
                    })
                    break

        return result

    def get_vehicle_type(self, obj):
        if not obj.vehicle_type:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.vehicle_type)
        
        # VEHICLE_TYPE_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in VEHICLE_TYPE_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None
    
    def get_driving_training_location(self, obj):
        if not obj.driving_training_location:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.driving_training_location)
        
        # DRIVING_TRAINING_LOCATION_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in DRIVING_TRAINING_LOCATION_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None


        


class BeneficiaryWillingnessInfoSerializer(serializers.ModelSerializer):
    livelihood_plan = serializers.SerializerMethodField()
    employment_challenge_type = serializers.SerializerMethodField()
    onsite_training_challenge_types = serializers.SerializerMethodField()
    
    class Meta:
        model = BeneficiaryWillingnessInfo
        fields = '__all__'
    
    def get_livelihood_plan(self, obj):
        if not obj.livelihood_plan:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.livelihood_plan)
        
        # LIVELIHOOD_PLAN_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in LIVELIHOOD_PLAN_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None

    def get_employment_challenge_type(self, obj):
        raw_val = obj.employment_challenge_type
        if not raw_val:
            return []

        # ডাটাবেজে ডাটা string ("1,2,3") নাকি list ([1, 2, 3]) হিসেবে আছে তা হ্যান্ডেল করা
        if isinstance(raw_val, str):
            selected_values = [v.strip() for v in raw_val.split(',') if v.strip()]
        elif isinstance(raw_val, list):
            selected_values = [str(v) for v in raw_val]
        else:
            selected_values = [str(raw_val)]

        result = []
        options = EMPLOYMENT_CHALLENGE_TYPE_CONFIG.get('options', [])

        # সেলেক্টেড ভ্যালুগুলোর সাথে ম্যাচ করে labelEn এবং labelBn সহ অবজেক্ট তৈরি করা
        for val in selected_values:
            for option in options:
                if str(option.get('value')) == val:
                    result.append({
                        "value": option.get('value'),
                        "labelEn": option.get('labelEn'),
                        "labelBn": option.get('labelBn')
                    })
                    break

        return result

    def get_onsite_training_challenge_types(self, obj):
        raw_val = obj.onsite_training_challenge_types
        if not raw_val:
            return []

        # ডাটাবেজে ডাটা string ("1,2,3") নাকি list ([1, 2, 3]) হিসেবে আছে তা হ্যান্ডেল করা
        if isinstance(raw_val, str):
            selected_values = [v.strip() for v in raw_val.split(',') if v.strip()]
        elif isinstance(raw_val, list):
            selected_values = [str(v) for v in raw_val]
        else:
            selected_values = [str(raw_val)]

        result = []
        options = ONSITE_TRAINING_CHALLENGE_TYPE_CONFIG.get('options', [])

        # সেলেক্টেড ভ্যালুগুলোর সাথে ম্যাচ করে labelEn এবং labelBn সহ অবজেক্ট তৈরি করা
        for val in selected_values:
            for option in options:
                if str(option.get('value')) == val:
                    result.append({
                        "value": option.get('value'),
                        "labelEn": option.get('labelEn'),
                        "labelBn": option.get('labelBn')
                    })
                    break

        return result

    
# ==============================================================================
# 3. BENEFICIARY SERIALIZERS (List, Detail & Write)
# ==============================================================================

class BeneficiarySerializer(serializers.ModelSerializer):
    """
    Lightweight Serializer for Data-Grid / Table List View.
    """
    district_name = serializers.CharField(source='geo_location.district.name_bn', read_only=True, default=None)
    upazila_name = serializers.CharField(source='geo_location.upazila.name_bn', read_only=True, default=None)
    union_name = serializers.CharField(source='geo_location.union.name_bn', read_only=True, default=None)
    gender_display = serializers.CharField(source='applicant_gender.label_bn', read_only=True, default=None)
    package_display = serializers.CharField(source='package.name_bn', read_only=True, default=None)

    class Meta:
        model = BeneficiaryInfo
        fields = [
            'id',
            'package_display',
            'response_id',
            'applicant_name_en',
            'applicant_name_bn',
            'mobile_self',
            'district_name',
            'upazila_name',
            'union_name',
            'gender_display',
            'status',
            'created_at'
        ]


class BeneficiaryDetailSerializer(serializers.ModelSerializer):
    """
    Complete Nested Serializer for Profile / Detail View.
    """
    applicant_gender = GenderSerializer(read_only=True)
    geo_location = BeneficiaryGeoLocationSerializer(read_only=True)
    household_info = BeneficiaryHouseHoldInfoSerializer(read_only=True)
    difficulty_profile = BeneficiaryDifficultySerializer(read_only=True)
    edu_info = BeneficiaryEducationInfoSerializer(read_only=True)
    employment_info = BeneficiaryEmploymentInfoSerializer(read_only=True)
    digital_skill = BeneficiaryDigitalSkillSerializer(read_only=True)
    willingness_info = BeneficiaryWillingnessInfoSerializer(read_only=True)

    marital_status = serializers.SerializerMethodField()
    no_nid_declaration = serializers.SerializerMethodField()
    relation_to_hh_head = serializers.SerializerMethodField()
    

    class Meta:
        model = BeneficiaryInfo
        fields = '__all__'
    
    def get_marital_status(self, obj):
        if not obj.marital_status:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.marital_status)
        
        # MARITAL_STATUS_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in MARITAL_STATUS_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None

    def get_relation_to_hh_head(self, obj):
        if not obj.relation_to_hh_head:
            return None
        
        # database-এর value (যেমন "1" বা 1) কে string এ কনভার্ট করা
        status_val = str(obj.relation_to_hh_head)
        
        # RELATION_TO_HH_HEAD_CONFIG থেকে ম্যাচ হওয়া অপশন খুঁজে অবজেক্ট তৈরি করা
        for option in RELATION_TO_HH_HEAD_CONFIG.get('options', []):
            if str(option.get('value')) == status_val:
                return {
                    "value": option.get('value'),
                    "labelEn": option.get('labelEn'),
                    "labelBn": option.get('labelBn')
                }
                
        return None

    def get_no_nid_declaration(self, obj):
        # মান যদি 0 হয় তবে 'এনআইডি', 1 হলে 'জন্ম নিবন্ধন'
        if obj.no_nid_declaration == 0:
            return "এনআইডি"
        elif obj.no_nid_declaration == 1:
            return "জন্ম নিবন্ধন"
        
        return None


class BeneficiaryWriteSerializer(serializers.ModelSerializer):
    """
    Writable Serializer for Create and Update actions.
    """
    class Meta:
        model = BeneficiaryInfo
        fields = '__all__'