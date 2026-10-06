import uuid
from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import Gender
from apps.core.constants import (RELATION_TO_HH_HEAD_CONFIG, MARITAL_STATUS_CONFIG, 
HOUSEHOLE_SPECIAL_AREA_CONFIG, DIFFICULTY_SEEING_CHOICES, DIFFICULTY_HEARING_CHOICES, 
DIFFICULTY_WALKING_CHOICES, DIFFICULTY_REMEMBERING_CHOICES, 
DIFFICULTY_SELFCARE_CHOICES, DIFFICULTY_COMMUNICATING_CHOICES)
from apps.core.constants import (
    HH_COUNT_UNCOLLECTED_REASON_CONFIG, 
    HIGHEST_EDUCATION_LEVEL_CONFIG_CHOICES,
    INSTITUTION_TYPE_CHOICES,
    MADRASHA_TYPE_CHOICES,
    DISCONTINUE_REASON_CHOICES,
    EMPLOYMENT_STATUS_CHOICES,
    SELF_EMPLOYMENT_TYPE_CHOICES,
    WAGE_EMPLOYMENT_STATUS_CHOICES,
    UNEMPLOYED_DURATION_CHOICES,
    WORK_EXPERIENCE_CHOICES,
    REASON_FOR_LEAVE_CHOICES,
    TRAINING_PROJECT_NAME_CHOICES,
    TRAINING_MONTHS_AGO_CHOICES,
    COMPUTER_SKILL_CHOICES,
    VEHICLE_TYPE_CHOICES,
    DRIVING_TRAINING_LOCATION_CHOICES,
    LIVELIHOOD_PLAN_CHOICES
    )


# ==========================================
# 1. Geo Location Model (core.Location-এর সাথে Linked)
# ==========================================
class BeneficiaryGeoLocation(models.Model):
    id = models.BigAutoField(primary_key=True)

    # BeneficiaryInfo-এর সাথে 1-to-1 রিলেশনশিপ
    beneficiary = models.OneToOneField(
        'BeneficiaryInfo',
        on_delete=models.CASCADE,
        related_name='geo_location',
        db_column='beneficiary_info_id'
    )

    # Core Location Foreign Keys
    division = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='geo_divisions',
        to_field='location_id',
        db_column='division_id',
        verbose_name="Division"
    )
    district = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='geo_districts',
        to_field='location_id',
        db_column='district_id',
        verbose_name="District"
    )
    upazila = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='geo_upazilas',
        to_field='location_id',
        db_column='upazila_id',
        verbose_name="Upazila"
    )
    
    # Pouro/Union Indicator Field (যেমন: 1 = Union, 2 = Pourashava)
    pouroword_or_union = models.SmallIntegerField(null=True, blank=True, verbose_name="Pouro/Word or Union Type")

    union = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='geo_unions',
        to_field='location_id',
        db_column='union_id',
        verbose_name="Union / Ward Location"
    )

    ward_no = models.CharField(max_length=50, null=True, blank=True, verbose_name="Ward No")

    village = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='geo_villages',
        to_field='location_id',
        db_column='village_id',
        verbose_name="Village Location"
    )
    
    # মাস্টার ডাটাতে গ্রাম না থাকলে ম্যানুয়াল টেক্সট
    village_other = models.CharField(max_length=255, null=True, blank=True, verbose_name="Village (Other)")

    # Household & Coordinates
    household_identification = models.CharField(max_length=100, null=True, blank=True, verbose_name="Household Identification")
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True, verbose_name="Longitude")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_geo_location'
        verbose_name = 'Beneficiary Geo Location'
        verbose_name_plural = 'Beneficiary Geo Locations'

    def __str__(self):
        return f"GeoLocation for Beneficiary ID: {self.beneficiary_id}"


# ==========================================
# 2. Beneficiary Info Model
# ==========================================
class BeneficiaryInfo(models.Model):
    # Primary Key
    id = models.BigAutoField(primary_key=True)

    # Foreign Key to Project Model
    # 'projects.Project' এর জায়গায় আপনার প্রজেক্ট মডেলের অ্যাপ ও ক্লাসের নাম দিন
    projects_project = models.ForeignKey(
        'projects.Project', 
        on_delete=models.CASCADE,
        db_column='projects_project_id',
        related_name='beneficiaries',
        null=True,
        blank=True
    )

    # Package Foreign Key
    package = models.ForeignKey(
        'core.Package',
        on_delete=models.SET_NULL,  # প্যাকেজ ডিলিট হলেও বেনিফিশিয়ারি থাকবে
        null=True,
        blank=True,
        related_name='beneficiaries',
        db_column='package_id',
        verbose_name="Package"
    )

    # Basic Info & Identifiers
    is_consent_given = models.BooleanField(default=True, verbose_name="Is Consent Given")
    
    # Python 3.14+ UUIDv7
    response_id = models.CharField(
        max_length=100,
        unique=True, 
        db_index=True, 
        verbose_name="Response ID"
    )
    
    applicant_name_en = models.CharField(max_length=255, null=True, blank=True, verbose_name="Applicant Name (EN)")
    applicant_name_bn = models.CharField(max_length=255, null=True, blank=True, verbose_name="Applicant Name (BN)")

    # NID / BRN Details
    no_nid_declaration = models.BooleanField(default=False, verbose_name="No NID Declaration")
    applicant_nid = models.CharField(max_length=20, null=True, blank=True, db_index=True,  verbose_name="Applicant NID")
    applicant_brn = models.CharField(max_length=20, null=True, blank=True, db_index=True, verbose_name="Applicant BRN")

    # Age & Date of Birth
    applicant_dob = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    applicant_age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Age")

    # Mobile Information
    mobile_owner = models.CharField(max_length=100, null=True, blank=True)
    mobile_self = models.CharField(max_length=15, null=True, blank=True, verbose_name="Mobile Self")
    mobile_request = models.CharField(max_length=15, null=True, blank=True, verbose_name="Mobile Request")

    # Demographics & Household Relation
   
    applicant_gender = models.ForeignKey(
        'core.Gender',  # core অ্যাপের Gender মডেল
        on_delete=models.SET_NULL,  # Gender ডিলিট হলেও বেনিফিশিয়ারি মুছে যাবে না
        null=True,
        blank=True,
        related_name='beneficiaries',
        db_column='applicant_gender_id',
        verbose_name="Applicant Gender"
    )
    RELATION_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in RELATION_TO_HH_HEAD_CONFIG['options']
    ]

    relation_to_hh_head = models.IntegerField(
        choices=RELATION_CHOICES,
        null=True,
        blank=True,
        verbose_name="Relation to Household Head"
    )

    relation_to_hh_head_others = models.CharField(max_length=255, null=True, blank=True, verbose_name="Relation to HH Head (Others)")
    
    MARITAL_STATUS_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in MARITAL_STATUS_CONFIG['options']
    ]
    marital_status = models.IntegerField(
        choices=MARITAL_STATUS_CHOICES,
        null=True,
        blank=True,
        verbose_name="Marital Status"
    )

    # Children & Support Info
    has_children = models.BooleanField(default=False, verbose_name="Has Children")
    children_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Children Count")
    has_dependent_children = models.BooleanField(default=False, verbose_name="Has Dependent Children")
    has_childcare_support = models.BooleanField(default=False, verbose_name="Has Childcare Support")

    # Data Collection & Enumerator Meta
    data_collection_date = models.DateField(null=True, blank=True, verbose_name="Data Collection Date")
    comments_of_enumerator = models.TextField(null=True, blank=True, verbose_name="Comments of Enumerator")
    enumerator_organization_en = models.CharField(max_length=255, null=True, blank=True, verbose_name="Enumerator Organization (EN)")

    # Status Field
    status = models.SmallIntegerField(default=1, verbose_name="Status")

    # Timestamps (Best practice)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_info'
        verbose_name = 'Beneficiary Info'
        verbose_name_plural = 'Beneficiary Info List'

    def __str__(self):
        return f"{self.applicant_name_en} ({self.response_id})"


# ==========================================
# 3. Beneficiary Attachments Model
# ==========================================
class BeneficiaryAttachment(models.Model):
    id = models.BigAutoField(primary_key=True)

    # BeneficiaryInfo-এর সাথে 1-to-1 রিলেশনশিপ
    beneficiary = models.OneToOneField(
        'BeneficiaryInfo',
        on_delete=models.CASCADE,
        related_name='attachment',
        db_column='beneficiary_info_id'
    )

    # Status Flags (1 / 0) - ডকুমেন্টস জমা আছে কিনা তা নির্দেশ করার জন্য
    attachment_photo = models.BooleanField(default=False, verbose_name="Photo Attached (1/0)")
    attachment_nid_doc = models.BooleanField(default=False, verbose_name="NID Doc Attached (1/0)")
    attachment_brn_doc = models.BooleanField(default=False, verbose_name="BRN Doc Attached (1/0)")
    attachment_hh_head_nid_doc = models.BooleanField(default=False, verbose_name="HH Head NID Doc Attached (1/0)")
    attachment_testimonial_or_certificate = models.BooleanField(default=False, verbose_name="Testimonial/Certificate Attached (1/0)")

    # File / Image Upload Fields (ডকুমেন্ট ফাইল বা পাথ সেভ করার জন্য)
    education_certificate = models.FileField(
        upload_to='beneficiaries/certificates/education/',
        null=True,
        blank=True,
        verbose_name="Education Certificate File"
    )
    testimonial = models.FileField(
        upload_to='beneficiaries/testimonials/',
        null=True,
        blank=True,
        verbose_name="Testimonial File"
    )
    training_certificate = models.FileField(
        upload_to='beneficiaries/certificates/training/',
        null=True,
        blank=True,
        verbose_name="Training Certificate File"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_attachment'
        verbose_name = 'Beneficiary Attachment'
        verbose_name_plural = 'Beneficiary Attachments'

    def __str__(self):
        return f"Attachments for Beneficiary ID: {self.beneficiary_id}"

# ==========================================
# 5. Beneficiary House Hold Info Model
# ==========================================    
class BeneficiaryHouseHoldInfo(models.Model):
    beneficiary = models.OneToOneField(
        'BeneficiaryInfo',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='household_info'
    )
    
    # 10. খানা প্রধানের নাম
    hh_head_name_en = models.CharField(max_length=255, blank=True, null=True)
    hh_head_name_bn = models.CharField(max_length=255, blank=True, null=True)
    
    # 11. খানা প্রধানের লিঙ্গ
    hh_head_gender = models.ForeignKey(
        'core.Gender',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='hh_head_genders',
        verbose_name="Household Head Gender"
    )
    
    # 12. খানা প্রধানের এনআইডি নম্বর
    hh_head_nid = models.CharField(max_length=50, blank=True, null=True,  db_index=True, verbose_name="Household Head NID")
    
    # 13-17. সদস্য সংক্রান্ত তথ্য
    hh_total_members = models.PositiveIntegerField(default=0)
    hh_count_1535 = models.PositiveIntegerField(default=0)
    hh_count_1535_collected = models.PositiveIntegerField(default=0)

    HH_COUNT_UNCOLLECTED_REASON_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in HH_COUNT_UNCOLLECTED_REASON_CONFIG['options']
    ]
    hh_count_1535_uncollected_reason = models.CharField(
        max_length=255, 
        null=True, 
        blank=True,  verbose_name="Reason for Uncollected (Multiple)")
    hh_count_earning = models.PositiveIntegerField(default=0)
    
    # 18-19. ক্ষুদ্র নৃ-গোষ্ঠী তথ্য
    is_indigenous = models.BooleanField(default=False)
    indigenous_group_type = models.ForeignKey(
        'core.IndigenousGroupType',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='household_indigenous_groups',
        verbose_name="Indigenous Group Type"
    )
    indigenous_group_others = models.CharField(max_length=255, blank=True, null=True)
    
    # 20-21. বিশেষ এলাকা
    SPECIAL_AREA_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
            for opt in HOUSEHOLE_SPECIAL_AREA_CONFIG['options']
        ]
    household_special_area = models.IntegerField(blank=True, null=True, choices=SPECIAL_AREA_CHOICES, verbose_name="Household Special Area")
    household_special_area_specify = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'beneficiary_house_hold_info'
        verbose_name = 'Beneficiary Household Info'
        verbose_name_plural = 'Beneficiary Household Infos'

    def __str__(self):
        return f"Household for {self.beneficiary.applicant_name_en or self.beneficiary.id}"



class BeneficiaryDifficulty(models.Model):
    beneficiary = models.OneToOneField(
        'BeneficiaryInfo',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='difficulty_profile'
    )
    seeing = models.IntegerField(choices=DIFFICULTY_SEEING_CHOICES, null=True, blank=True, db_index=True)
    hearing = models.IntegerField( choices=DIFFICULTY_HEARING_CHOICES, null=True, blank=True, db_index=True)
    walking = models.IntegerField(choices=DIFFICULTY_WALKING_CHOICES, null=True, blank=True, db_index=True)
    remembering = models.IntegerField(choices=DIFFICULTY_REMEMBERING_CHOICES, null=True, blank=True, db_index=True)
    selfcare = models.IntegerField(choices=DIFFICULTY_SELFCARE_CHOICES, null=True, blank=True, db_index=True)
    communicating = models.IntegerField( choices=DIFFICULTY_COMMUNICATING_CHOICES, null=True, blank=True, db_index=True)
    is_pwd = models.BooleanField(default=False, verbose_name="Is Person with Disability")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_difficulty'
        verbose_name = 'Beneficiary Difficulty'
        verbose_name_plural = 'Beneficiary Difficulties'

    def __str__(self):
        return f"Difficulty Profile - Beneficiary ID: {self.beneficiary_id}"

# ==========================================
# 5. Beneficiary Education Info Model
# ==========================================
class BeneficiaryEducationInfo(models.Model):
    
    beneficiary = models.OneToOneField(
        'BeneficiaryInfo',
        on_delete=models.CASCADE,
         primary_key=True,
        related_name='edu_info'
    )

    # Education Details
    currently_in_education = models.BooleanField(null=True, blank=True, verbose_name="Currently in Education")
    highest_education_level = models.SmallIntegerField(choices=HIGHEST_EDUCATION_LEVEL_CONFIG_CHOICES, null=True, blank=True, verbose_name="Highest Education Level")
    other_education_level = models.CharField(max_length=255, null=True, blank=True, verbose_name="Other Education Level")
    institution_type = models.SmallIntegerField(choices=INSTITUTION_TYPE_CHOICES, null=True, blank=True, verbose_name="Institution Type")
    madrasha_type = models.SmallIntegerField(choices=MADRASHA_TYPE_CHOICES, null=True, blank=True, verbose_name="Madrasha Type")
    attended_classes_last_6_months = models.BooleanField(null=True, blank=True, verbose_name="Attended Classes Last 6 Months")
    ever_dropped_out = models.BooleanField(null=True, blank=True, verbose_name="Ever Dropped Out")
    # discontinue_reason = models.SmallIntegerField(choices=DISCONTINUE_REASON_CHOICES, null=True, blank=True, verbose_name="Discontinue Reason")
    discontinue_reason = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Discontinue Reason"
    )
    discontinue_reason_others = models.CharField(max_length=255, null=True, blank=True, verbose_name="Discontinue Reason Others")
    attended_govt_job_exam_last_6_months = models.BooleanField(null=True, blank=True, verbose_name="Attended Govt Job Exam Last 6 Months")

    # Literacy Skills
    can_read_bangla = models.BooleanField(null=True, blank=True, verbose_name="Can Read Bangla")
    can_write_bangla = models.BooleanField(null=True, blank=True, verbose_name="Can Write Bangla")
    can_read_english = models.BooleanField(null=True, blank=True, verbose_name="Can Read English")
    can_write_english = models.BooleanField(null=True, blank=True, verbose_name="Can Write English")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_education_info'
        verbose_name = 'Beneficiary Education Info'
        verbose_name_plural = 'Beneficiary Education Infos'

    def __str__(self):
        return f"Edu Info for Beneficiary ID: {self.beneficiary_id}"


# ==========================================
# 6. Beneficiary Employment Info Model
# ==========================================
class BeneficiaryEmploymentInfo(models.Model):
   
    beneficiary = models.OneToOneField(
        'BeneficiaryInfo',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='employment_info'
    )
    # Current Employment Details
    is_currently_employed = models.BooleanField(null=True, blank=True, verbose_name="Is Currently Employed")
    employment_status_self_or_wage = models.SmallIntegerField(choices=EMPLOYMENT_STATUS_CHOICES, null=True, blank=True, verbose_name="Employment Status (Self/Wage)")
    current_employment_type = models.SmallIntegerField(choices=SELF_EMPLOYMENT_TYPE_CHOICES, null=True, blank=True, verbose_name="Current Employment Type")
    wage_employment_status = models.SmallIntegerField(choices=WAGE_EMPLOYMENT_STATUS_CHOICES, null=True, blank=True, verbose_name="Wage Employment Status")
    employment_status_others = models.CharField(max_length=255, null=True, blank=True, verbose_name="Employment Status Others")
    # Income & Unemployment Details
    income_last_month = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Income Last Month")
    avg_income_6months = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Average Income Last 6 Months")
    unemployment_months = models.PositiveIntegerField(choices=UNEMPLOYED_DURATION_CHOICES, null=True, blank=True, verbose_name="Unemployment Months")
    # Past Work Experience Details
    has_work_experience = models.BooleanField(null=True, blank=True, verbose_name="Has Work Experience")
    experience_years = models.SmallIntegerField(choices=WORK_EXPERIENCE_CHOICES, null=True, blank=True, verbose_name="Experience (Years)")
    left_work_reason = models.SmallIntegerField(choices=REASON_FOR_LEAVE_CHOICES, null=True, blank=True, verbose_name="Left Work Reason")
    left_work_reason_others = models.CharField(max_length=255, null=True, blank=True, verbose_name="Left Work Reason Others")

    # Training Details
    currently_in_training = models.BooleanField(null=True, blank=True, verbose_name="Currently in Training")
    received_skill_training_go_ngo = models.BooleanField(null=True, blank=True, verbose_name="Received Skill Training GO/NGO")
    has_vocational_certificate = models.BooleanField(null=True, blank=True, verbose_name="Has Vocational Certificate")
    training_project_name = models.SmallIntegerField(choices=TRAINING_PROJECT_NAME_CHOICES, null=True, blank=True, verbose_name="Training Project Name")
    training_project_name_others = models.CharField(max_length=255, null=True, blank=True, verbose_name="Training Project Name Others")
    training_months_ago = models.SmallIntegerField(choices=TRAINING_MONTHS_AGO_CHOICES, null=True, blank=True, verbose_name="Training Months Ago")
    training_trade = models.CharField(max_length=255, null=True, blank=True, verbose_name="Training Trade")

    # Beneficiary Qualification
    is_potential_beneficiary = models.BooleanField(null=True, blank=True, verbose_name="Is Potential Beneficiary")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_employment_info'
        verbose_name = 'Beneficiary Employment Info'
        verbose_name_plural = 'Beneficiary Employment Infos'

    def __str__(self):
        return f"Employment Info for Beneficiary ID: {self.beneficiary_id}"

# ==========================================
# 7. Beneficiary Digital Skill Model
# ==========================================
class BeneficiaryDigitalSkill(models.Model):
    beneficiary = models.OneToOneField(
        'BeneficiaryInfo',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='digital_skill'
    )
    
    # 67. স্মার্টফোন আছে কিনা
    has_smartphone = models.BooleanField(null=True, blank=True, verbose_name="Has Smartphone")
    
    # 68. কম্পিউটার/ল্যাপটপ আছে কিনা
    has_computer_or_laptop = models.BooleanField(null=True, blank=True, verbose_name="Has Computer or Laptop")
    
    # 69. কম্পিউটার চালনায় দক্ষতা (1: শিক্ষানবিশ/মৌলিক, 2: মধ্যম, 3: উন্নত/দক্ষ ইত্যাদি)
    computer_skill = models.SmallIntegerField(choices=COMPUTER_SKILL_CHOICES, null=True, blank=True, verbose_name="Computer Skill Level")
    
    # 70. ইন্টারনেট ব্যবহার করেন কিনা
    uses_internet = models.BooleanField(null=True, blank=True, verbose_name="Uses Internet")
    
    # 71. অ্যাপগুলোর ব্যবহার (মাল্টিপল হতে পারে তাই CharField হিসেবে রাখা ভালো)
    app_usage = models.CharField(max_length=255, null=True, blank=True, verbose_name="App Usage")
    
    # 72. গাড়ি চালানো জানেন কিনা
    knows_driving = models.BooleanField(null=True, blank=True, verbose_name="Knows Driving")
    
    # 73. যানবাহনের ধরন
    vehicle_type = models.SmallIntegerField(choices=VEHICLE_TYPE_CHOICES, null=True, blank=True, verbose_name="Vehicle Type")
    
    # 74. ড্রাইভিং লাইসেন্স আছে কিনা
    has_driving_licence = models.BooleanField(null=True, blank=True, verbose_name="Has Driving Licence")
    
    # 75. ড্রাইভিং প্রশিক্ষণ নিয়েছেন কিনা
    received_driving_training = models.BooleanField(null=True, blank=True, verbose_name="Received Driving Training")
    
    # 76. প্রশিক্ষণের স্থান
    driving_training_location = models.SmallIntegerField(choices=DRIVING_TRAINING_LOCATION_CHOICES, null=True, blank=True, verbose_name="Driving Training Location")
    
    # 76.1 অন্যান্য হলে প্রশিক্ষণের স্থান
    driving_training_location_others = models.CharField(max_length=255, null=True, blank=True, verbose_name="Driving Training Location Others")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_digital_skill'
        verbose_name = 'Beneficiary Digital Skill'
        verbose_name_plural = 'Beneficiary Digital Skills'

    def __str__(self):
        return f"Digital Skill for Beneficiary ID: {self.beneficiary_id}"

# ==========================================
# 8. Beneficiary Willingness Info Model
# ==========================================
class BeneficiaryWillingnessInfo(models.Model):
    beneficiary = models.OneToOneField(
        'BeneficiaryInfo',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='willingness_info'
    )

    # 77. জীবিকা নিয়ে এখন আপনার পরিকল্পনা কী?
    livelihood_plan = models.SmallIntegerField(
        choices=LIVELIHOOD_PLAN_CHOICES, 
        null=True, 
        blank=True, 
        verbose_name="Livelihood Plan"
    )

    # 78. আপনি কি বর্তমানে কোনো কর্মসংস্থান বা ব্যবসার সুযোগ খুঁজছেন?
    searching_employment = models.BooleanField(
        null=True, 
        blank=True, 
        verbose_name="Searching Employment/Business"
    )

    # 79. আপনি কি চাকরি বা ব্যবসায় যুক্ত হতে কোনো বাধার সম্মুখীন হচ্ছেন?
    has_employment_challenges = models.BooleanField(
        null=True, 
        blank=True, 
        verbose_name="Has Employment Challenges"
    )

    # 80. যদি হ্যাঁ হয়, তাহলে সেগুলো কী কী? (Comma-separated text for multiple choices)
    employment_challenge_type = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Employment Challenge Types"
    )

    # 80.1 অন্যান্য চ্যালেঞ্জ লিখুন
    employment_challenge_others = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Employment Challenge Others"
    )

    # 81. আপনি কি আপনার কর্মসংস্থান তৈরির জন্য কোনো আনুষ্ঠানিক প্রশিক্ষণে অংশ নিতে আগ্রহী?
    interested_in_training = models.BooleanField(
        null=True, 
        blank=True, 
        verbose_name="Interested in Formal Training"
    )

    # 82. আপনার এলাকায় সরাসরি প্রশিক্ষণে অংশগ্রহণ করতে কি কোনো অসুবিধা আছে?
    has_onsite_training_challenges = models.BooleanField(
        null=True, 
        blank=True, 
        verbose_name="Has Onsite Training Challenges"
    )

    # 83. যদি হ্যাঁ হয়, তাহলে সেগুলো কী কী? (Comma-separated text for multiple choices)
    onsite_training_challenge_types = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Onsite Training Challenge Types"
    )

    # 83.1 অন্যান্য চ্যালেঞ্জ লিখুন
    onsite_training_challenge_others = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name="Onsite Training Challenge Others"
    )

    # 84. আপনি কি অনলাইন প্রশিক্ষণে অংশগ্রহণ করতে স্বাচ্ছন্দ্যবোধ করেন?
    comfortable_online_training = models.BooleanField(
        null=True, 
        blank=True, 
        verbose_name="Comfortable with Online Training"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'beneficiary_willingness_info'
        verbose_name = 'Beneficiary Willingness Info'
        verbose_name_plural = 'Beneficiary Willingness Infos'

    def __str__(self):
        return f"Willingness Info for Beneficiary ID: {self.beneficiary_id}"
