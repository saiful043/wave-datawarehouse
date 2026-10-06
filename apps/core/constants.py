from django.db import models
from django.utils.translation import gettext_lazy as _

# ==============================================================================
# 1. Reason Data Not Collected Config & Choices
# ==============================================================================

# 1. Django Models / Serializers-এ ব্যবহারের জন্য TextChoices
class HHCountUncollectedReasonChoices(models.TextChoices):
    NOT_AVAILABLE = '1', _('Not available / পাওয়া যায়নি')
    NOT_POTENTIAL = '2', _('Not potential beneficiary / সম্ভাব্য সুবিধাভোগী নয়')
    REFUSED = '3', _('Refused to provide information / তথ্য দিতে অস্বীকৃতি জানিয়েছেন')


# 2. Next.js Frontend UI-এর জন্য ডিরেক্ট JSON Payload Structure
HH_COUNT_UNCOLLECTED_REASON_CONFIG = {
    "headerNameEn": "Reason Data Not Collected",
    "headerNameBn": "তথ্য সংগ্রহ না হওয়ার কারণ",
    "options": [
        {
            "value": "1",
            "labelEn": "Not available",
            "labelBn": "পাওয়া যায়নি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Not potential beneficiary",
            "labelBn": "সম্ভাব্য সুবিধাভোগী নয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
              "labelEn": "Refused to provide information",
            "labelBn": "তথ্য দিতে অস্বীকৃতি জানিয়েছেন",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        }
    ]
}


# ==============================================================================
# 2. Special Area Type Config & Choices
# ==============================================================================

class HouseholdSpecialAreaChoices(models.TextChoices):
    TEA_GARDENS = '1', _('Tea gardens / চা বাগান')
    HAORS = '2', _('Haors / হাওর')
    CHARS = '3', _('Chars / চর')
    HILL_TRACTS = '4', _('Hill-tracts / পার্বত্য অঞ্চল')
    COASTAL_BELT = '5', _('Coastal belt / উপকূলীয় অঞ্চল')
    NONE_OF_THE_ABOVE = '6', _('None of the above / উপরের কোনোটিই নয়')


HOUSEHOLE_SPECIAL_AREA_CONFIG = {
    "headerNameEn": "Special Area Type",
    "headerNameBn": "বিশেষ অঞ্চলের ধরন",
    "placeholderEn": "Select area",
    "placeholderBn": "এলাকা নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "Tea gardens",
            "labelBn": "চা বাগান",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Haors",
            "labelBn": "হাওর",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "Chars",
            "labelBn": "চর",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "Hill-tracts",
            "labelBn": "পার্বত্য অঞ্চল",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "5",
            "labelEn": "Coastal belt",
            "labelBn": "উপকূলীয় অঞ্চল",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        },
        {
            "value": "6",
            "labelEn": "None of the above",
            "labelBn": "উপরের কোনোটিই নয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 6,
            "visibleWhen": None
        }
    ]
}

# ==============================================================================
# Relation to Household Head Choices & Config
# ==============================================================================
class RelationToHHHeadChoices(models.TextChoices):
    HOUSEHOLD_HEAD = '12', _('Household Head / খানা প্রধান')
    HUSBAND_WIFE = '13', _('Husband/Wife / স্বামী/স্ত্রী')
    SON_DAUGHTER = '14', _('Son/Daughter / পুত্র/কন্যা')
    SPOUSE_OF_SON_DAUGHTER = '15', _('Spouse of Son/Daughter / পুত্র/কন্যার স্বামী/স্ত্রী')
    GRANDFATHER_GRANDMOTHER = '16', _('Grandfather/grandmother / দাদা/দাদি/নানা/নানি')
    FATHER_MOTHER = '17', _('Father/Mother / পিতা/মাতা')
    BROTHER_SISTER = '18', _('Brother/Sister / ভাই/বোন')
    NIECE_NEPHEW = '19', _('Niece/Nephew / ভাতিজা/ভাতিজি')
    FATHER_MOTHER_IN_LAW = '20', _('Father/Mother-in-law / শ্বশুর/শাশুড়ি')
    BROTHER_SISTER_IN_LAW = '21', _('Brother/Sister-in-law / দেওর/ভাবি/শালা/শালী')
    OTHER_RELATIVE = '204', _('Other relative / অন্যান্য আত্মীয়')
    OTHER = '22', _('Other (specify) / অন্যান্য (নির্দিষ্ট করুন)')


RELATION_TO_HH_HEAD_CONFIG = {
    "headerNameEn": "Head's Relation to Respondent",
    "headerNameBn": "উত্তরদাতার সাথে পরিবার প্রধানের সম্পর্ক",
    "placeholderEn": "Select relation",
    "placeholderBn": "সম্পর্ক নির্বাচন করুন",
    "options": [
        {
            "value": "12",
            "labelEn": "Household Head",
            "labelBn": "খানা প্রধান",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "13",
            "labelEn": "Husband/Wife",
            "labelBn": "স্বামী/স্ত্রী",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "14",
            "labelEn": "Son/Daughter",
            "labelBn": "পুত্র/কন্যা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "15",
            "labelEn": "Spouse of Son/Daughter",
            "labelBn": "পুত্র/কন্যার স্বামী/স্ত্রী",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "16",
            "labelEn": "Grandfather/grandmother",
            "labelBn": "দাদা/দাদি/নানা/নানি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        },
        {
            "value": "17",
            "labelEn": "Father/Mother",
            "labelBn": "পিতা/মাতা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 6,
            "visibleWhen": None
        },
        {
            "value": "18",
            "labelEn": "Brother/Sister",
            "labelBn": "ভাই/বোন",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 7,
            "visibleWhen": None
        },
        {
            "value": "19",
            "labelEn": "Niece/Nephew",
            "labelBn": "ভাতিজা/ভাতিজি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 8,
            "visibleWhen": None
        },
        {
            "value": "20",
            "labelEn": "Father/Mother-in-law",
            "labelBn": "শ্বশুর/শাশুড়ি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 9,
            "visibleWhen": None
        },
        {
            "value": "21",
            "labelEn": "Brother/Sister-in-law",
            "labelBn": "দেওর/ভাবি/শালা/শালী",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 10,
            "visibleWhen": None
        },
        {
            "value": "204",
            "labelEn": "Other relative",
            "labelBn": "অন্যান্য আত্মীয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 11,
            "visibleWhen": None
        },
        {
            "value": "22",
            "labelEn": "Other (specify)",
            "labelBn": "অন্যান্য (নির্দিষ্ট করুন)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 12,
            "visibleWhen": None
        }
    ]
}


# ==============================================================================
# 1. Marital Status Config & Choices
# ==============================================================================

class MaritalStatusChoices(models.TextChoices):
    UNMARRIED = '1', _('Unmarried / অবিবাহিত')
    MARRIED = '2', _('Married / বিবাহিত')
    DIVORCED_SEPARATED = '3', _('Divorced/Separated / তালাকপ্রাপ্ত/বিচ্ছিন্ন')
    ABANDONED = '4', _('Abandoned / পরিত্যক্ত')
    WIDOW_WIDOWER = '5', _('Widow/Widower / বিধবা/বিধুর')


MARITAL_STATUS_CONFIG = {
    "headerNameEn": "Marital Status",
    "headerNameBn": "বৈবাহিক অবস্থা",
    "placeholderEn": "Select marital status",
    "placeholderBn": "বৈবাহিক অবস্থা নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "Unmarried",
            "labelBn": "অবিবাহিত",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Married",
            "labelBn": "বিবাহিত",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "Divorced/Separated",
            "labelBn": "তালাকপ্রাপ্ত/বিচ্ছিন্ন",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "Abandoned",
            "labelBn": "পরিত্যক্ত",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "5",
            "labelEn": "Widow/Widower",
            "labelBn": "বিধবা/বিধুর",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        }
    ]
}

# ==============================================================================
# Highest Education Level Choices & Config
# ==============================================================================

class HighestEducationLevelChoices(models.TextChoices):
    NONE = '1', _('None / কোনো শিক্ষা নেই')
    BELOW_PRIMARY = '2', _('Below primary / প্রাথমিকে নিচে')
    CLASS_V_PASS = '3', _('Class V Pass/PEC/Ibtedai/Equivalent / পঞ্চম শ্রেণি পাস/পিইসি/ইবতেদায়ি/সমমান')
    CLASS_VIII_PASS = '4', _('Class VIII/JSC/JDC/Equivalent Pass / অষ্টম শ্রেণি/জেএসসি/জেডিসি/সমমান পাস')
    SSC_PASS = '5', _('SSC/Dakhil/O-Level/Equivalent Pass / এসএসসি/দাখিল/ও-লেভেল/সমমান পাস')
    HSC_PASS = '6', _('HSC/Alim/A-Level/Equivalent Pass / এইচএসসি/আলিম/এ-লেভেল/সমমান পাস')
    DIPLOMA_PASS = '7', _('Diploma Pass / ডিপ্লোমা পাস')
    NURSING_PASS = '8', _('Nursing/Midwifery Pass / নার্সিং/মিডওয়াইফারি পাস')
    DEGREE_PASS = '9', _('BA/BSc/BCom/BBA/Fazil (Pass Course) Pass / বিএ/বিএসসি/বিকম/বিবিএ/ফাজিল (পাস কোর্স) পাস')
    MASTERS_PASS = '10', _('MA/MSc/MCom/MBA/Kamil/Dawra and above Pass / এমএ/এমএসসি/এমকম/এমবিএ/কামিল/দাওরা ও তদূর্ধ্ব পাস')
    OTHERS = '11', _('Others (Specify) / অন্যান্য (নির্দিষ্ট করুন)')
    HONOURS_PASS = '12', _('BA/BSc/BCom/BBA (Hons) Pass / বিএ/বিএসসি/বিকম/বিবিএ (সম্মান) পাস')
    PHD_COMPLETED = '13', _('PhD Completed / পিএইচডি সম্পন্ন')
    MBBS_BDS_PASS = '14', _('MBBS/BDS Pass / এমবিবিএস/বিডিএস পাস')
    BSC_ENGINEERING_PASS = '15', _('BSc Engineering and above Pass / বিএসসি ইঞ্জিনিয়ারিং ও তদূর্ধ্ব পাস')
    NON_FORMAL_EDUCATION = '16', _('Non-formal/Informal Education / উপানুষ্ঠানিক/অনানুষ্ঠানিক শিক্ষা')


HIGHEST_EDUCATION_LEVEL_CONFIG = {
    "headerNameEn": "Highest Education Level",
    "headerNameBn": "সর্বোচ্চ শিক্ষাগত যোগ্যতা",
    "placeholderEn": "Select education level",
    "placeholderBn": "শিক্ষাগত যোগ্যতা নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "None",
            "labelBn": "কোনো শিক্ষা নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": {
                "fieldKey": "currently_in_education",
                "operator": "NotEquals",
                "value": 1,
                "dependsOn": "value"
            }
        },
        {
            "value": "2",
            "labelEn": "Below primary",
            "labelBn": "প্রাথমিকের নিচে",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "Class V Pass/PEC/Ibtedai/Equivalent",
            "labelBn": "পঞ্চম শ্রেণি পাস/পিইসি/ইবতেদায়ি/সমমান",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "Class VIII/JSC/JDC/Equivalent Pass",
            "labelBn": "অষ্টম শ্রেণি/জেএসসি/জেডিসি/সমমান পাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "5",
            "labelEn": "SSC/Dakhil/O-Level/Equivalent Pass",
            "labelBn": "এসএসসি/দাখিল/ও-লেভেল/সমমান পাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        },
        {
            "value": "6",
            "labelEn": "HSC/Alim/A-Level/Equivalent Pass",
            "labelBn": "এইচএসসি/আলিম/এ-লেভেল/সমমান পাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 6,
            "visibleWhen": None
        },
        {
            "value": "7",
            "labelEn": "Diploma Pass",
            "labelBn": "ডিপ্লোমা পাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 14,
            "visibleWhen": None
        },
        {
            "value": "8",
            "labelEn": "Nursing/Midwifery Pass",
            "labelBn": "নার্সিং/মিডওয়াইফারি পাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 12,
            "visibleWhen": None
        },
        {
            "value": "9",
            "labelEn": "BA/BSc/BCom/BBA/Fazil (Pass Course) Pass",
            "labelBn": "বিএ/বিএসসি/বিকম/বিবিএ/ফাজিল (পাস কোর্স) পাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 7,
            "visibleWhen": None
        },
        {
            "value": "10",
            "labelEn": "MA/MSc/MCom/MBA/Kamil/Dawra and above Pass",
            "labelBn": "এমএ/এমএসসি/এমকম/এমবিএ/কামিল/দাওরা ও তদূর্ধ্ব পাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 9,
            "visibleWhen": None
        },
        {
            "value": "11",
            "labelEn": "Others (Specify)",
            "labelBn": "অন্যান্য (নির্দিষ্ট করুন)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 16,
            "visibleWhen": None
        },
        {
            "value": "12",
            "labelEn": "BA/BSc/BCom/BBA (Hons) Pass",
            "labelBn": "বিএ/বিএসসি/বিকম/বিবিএ (সম্মান) পাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 8,
            "visibleWhen": None
        },
        {
            "value": "13",
            "labelEn": "PhD Completed",
            "labelBn": "পিএইচডি সম্পন্ন",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 10,
            "visibleWhen": None
        },
        {
            "value": "14",
            "labelEn": "MBBS/BDS Pass",
            "labelBn": "এমবিবিএস/বিডিএস পাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 11,
            "visibleWhen": None
        },
        {
            "value": "15",
            "labelEn": "BSc Engineering and above Pass",
            "labelBn": "বিএসসি ইঞ্জিনিয়ারিং ও তদূর্ধ্ব পাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 13,
            "visibleWhen": None
        },
        {
            "value": "16",
            "labelEn": "Non-formal/Informal Education",
            "labelBn": "উপানুষ্ঠানিক/অনানুষ্ঠানিক শিক্ষা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 15,
            "visibleWhen": None
        }
    ]
}

HIGHEST_EDUCATION_LEVEL_CONFIG_CHOICES = [
    (int(opt['value']), opt['labelEn']) 
    for opt in HIGHEST_EDUCATION_LEVEL_CONFIG['options']
]

# ==============================================================================
# Institution Type Choices & Config
# ==============================================================================

class InstitutionTypeChoices(models.TextChoices):
    GENERAL = '1', _('General / সাধারণ')
    MADRASHA = '2', _('Madrasha / মাদ্রাসা')
    TECHNICAL = '3', _('Technical / টেকনিক্যাল')
    PROFESSIONAL = '4', _('Professional / প্রফেশনাল')


INSTITUTION_TYPE_CONFIG = {
    "headerNameEn": "Institution Type",
    "headerNameBn": "প্রতিষ্ঠানের ধরন",
    "placeholderEn": "Select institution type",
    "placeholderBn": "প্রতিষ্ঠানের ধরন নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "General",
            "labelBn": "সাধারণ",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Madrasha",
            "labelBn": "মাদ্রাসা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "Technical",
            "labelBn": "টেকনিক্যাল",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "Professional",
            "labelBn": "প্রফেশনাল",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        }
    ]
}

INSTITUTION_TYPE_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in INSTITUTION_TYPE_CONFIG['options']
    ]


# ==============================================================================
# Madrasha Type Choices & Config
# ==============================================================================

class MadrashaTypeChoices(models.TextChoices):
    GOVT_APPROVED = '1', _('Government-approved madrasas / সরকার অনুমোদিত মাদ্রাসা')
    KOWMI = '2', _('Kowmi madrasas / কওমি মাদ্রাসা')


MADRASHA_TYPE_CONFIG = {
    "headerNameEn": "Madrasha Type",
    "headerNameBn": "মাদ্রাসার ধরন",
    "placeholderEn": "Select madrasha type",
    "placeholderBn": "মাদ্রাসার ধরন নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "Government-approved madrasas",
            "labelBn": "সরকার অনুমোদিত মাদ্রাসা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Kowmi madrasas",
            "labelBn": "কওমি মাদ্রাসা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        }
    ]
}

MADRASHA_TYPE_CHOICES = [
    (int(opt['value']), opt['labelEn']) 
    for opt in MADRASHA_TYPE_CONFIG['options']
]



# ==============================================================================
# Dropout Reason Choices & Config
# ==============================================================================

class DiscontinueReasonChoices(models.TextChoices):
    CLIMATE_INDUCED = '2', _('Climate induced dropouts / প্রাকৃতিক/আবহাওয়াজনিত')
    FINANCIAL = '3', _('Financial problem / আর্থিক সমস্যা')
    PHYSICAL = '4', _('Physical problem / শারীরিক সমস্যা')
    SOCIAL = '5', _('Social problem / সামাজিক সমস্যা')
    LACK_OF_WILLINGNESS = '6', _('Lack of willingness / ইচ্ছার অভাব')
    GOT_MARRIED = '7', _('Got married / বিয়ে হয়েছে')
    FAMILY_NOT_ALLOW = '8', _('Family does not allow / পরিবার অনুমতি দেয় না')
    MATERNITY_CHILDCARE = '9', _('Due to maternity/childcare / মাতৃত্বকালীন/শিশু পরিচর্যার কারণে')
    LOWER_GRADE_FAIL = '10', _('Due to lower grade/fail / নিম্ন গ্রেড/ফেলের কারণে')
    MIGRATION = '11', _('Migration / অভিবাসন')
    OTHERS = '14', _('Others (Specify) / অন্যান্য (নির্দিষ্ট করুন)')


DISCONTINUE_REASON_CONFIG = {
    "headerNameEn": "Discontinue Reason",
    "headerNameBn": "পড়াশোনা ছাড়ার কারণ",
    "placeholderEn": "Select dropout reason",
    "placeholderBn": "পড়াশোনা ছাড়ার কারণ নির্বাচন করুন",
    "options": [
        {
            "value": "2",
            "labelEn": "Climate induced dropouts",
            "labelBn": "প্রাকৃতিক/আবহাওয়াজনিত",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "Financial problem",
            "labelBn": "আর্থিক সমস্যা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "Physical problem (eg; disability, sickness etc.)",
            "labelBn": "শারীরিক সমস্যা (যেমন; অক্ষমতা, অসুস্থতা ইত্যাদি)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "5",
            "labelEn": "Social problem",
            "labelBn": "সামাজিক সমস্যা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "6",
            "labelEn": "Lack of willingness",
            "labelBn": "ইচ্ছার অভাব",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        },
        {
            "value": "7",
            "labelEn": "Got married",
            "labelBn": "বিয়ে হয়েছে",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 6,
            "visibleWhen": None
        },
        {
            "value": "8",
            "labelEn": "Family does not allow",
            "labelBn": "পরিবার অনুমতি দেয় না",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 7,
            "visibleWhen": None
        },
        {
            "value": "9",
            "labelEn": "Due to maternity/childcare",
            "labelBn": "মাতৃত্বকালীন/শিশু পরিচর্যার কারণে",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 8,
            "visibleWhen": None
        },
        {
            "value": "10",
            "labelEn": "Due to lower grade/fail",
            "labelBn": "নিম্ন গ্রেড/ফেলের কারণে",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 9,
            "visibleWhen": None
        },
        {
            "value": "11",
            "labelEn": "Migration",
            "labelBn": "অভিবাসন",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 10,
            "visibleWhen": None
        },
        {
            "value": "14",
            "labelEn": "Others (Specify)",
            "labelBn": "অন্যান্য (নির্দিষ্ট করুন)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 11,
            "visibleWhen": None
        }
    ]
}

DISCONTINUE_REASON_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in DISCONTINUE_REASON_CONFIG.get('options', [])
    ]

# ==============================================================================
# Employment Status Choices & Config
# ==============================================================================

class EmploymentStatusChoices(models.TextChoices):
    SELF_EMPLOYMENT = '1', _('Self-employment / স্ব-কর্মসংস্থান')
    WAGE_EMPLOYMENT = '2', _('Wage employment / মজুরি/বেতন ভিত্তিক কর্মসংস্থান')


EMPLOYMENT_STATUS_CONFIG = {
    "headerNameEn": "Employment Status",
    "headerNameBn": "কর্মসংস্থানের ধরন",
    "placeholderEn": "Select employment status",
    "placeholderBn": "কর্মসংস্থানের ধরন নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "Self-employment",
            "labelBn": "স্ব-কর্মসংস্থান",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Wage employment",
            "labelBn": "মজুরি/বেতন ভিত্তিক কর্মসংস্থান",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        }
    ]
}

EMPLOYMENT_STATUS_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in EMPLOYMENT_STATUS_CONFIG['options']
    ]

# ==============================================================================
# Self Employment Type Choices & Config
# ==============================================================================

class SelfEmploymentTypeChoices(models.TextChoices):
    FORMAL = '1', _('Formal / ফর্মাল')
    INFORMAL = '2', _('Informal / ইনফর্মাল')
    BUSINESS = '3', _('Business / ব্যবসা')


SELF_EMPLOYMENT_TYPE_CONFIG = {
    "headerNameEn": "Self-Employment Type",
    "headerNameBn": "স্ব-কর্মসংস্থানের ধরন",
    "placeholderEn": "Select self-employment type",
    "placeholderBn": "স্ব-কর্মসংস্থানের ধরন নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "Formal",
            "labelBn": "ফর্মাল",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Informal",
            "labelBn": "ইনফর্মাল",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "Business",
            "labelBn": "ব্যবসা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": {
                "fieldKey": "employment_status_self_or_wage",
                "operator": "NotEquals",
                "value": 2,
                "dependsOn": "value"
            }
        }
    ]
}

SELF_EMPLOYMENT_TYPE_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in SELF_EMPLOYMENT_TYPE_CONFIG['options']
    ]


# ==============================================================================
# Wage Employment Status Choices & Config
# ==============================================================================

class WageEmploymentStatusChoices(models.TextChoices):
    FULL_TIME = '1', _('Full-time paid employment / পূর্ণকালীন বেতনভোগী চাকরি')
    PART_TIME = '2', _('Part-time paid employment / খণ্ডকালীন বেতনভোগী চাকরি')
    CASUAL_DAILY_LABOR = '3', _('Casual/daily wage labor / অনিয়মিত/দিনমজুর')
    SEASONAL = '4', _('Seasonal employment / মৌসুমী কর্মসংস্থান')
    OTHERS = '5', _('Others (Specify) / অন্যান্য (নির্দিষ্ট করুন)')


WAGE_EMPLOYMENT_STATUS_CONFIG = {
    "headerNameEn": "Wage Employment Status",
    "headerNameBn": "মজুরি কর্মসংস্থানের ধরন",
    "placeholderEn": "Select wage employment status",
    "placeholderBn": "মজুরি কর্মসংস্থানের ধরন নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "Full-time paid employment (regular job with fixed working hours)",
            "labelBn": "পূর্ণকালীন বেতনভোগী চাকরি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Part-time paid employment (less than full-time working hours)",
            "labelBn": "খণ্ডকালীন বেতনভোগী চাকরি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "Casual/daily wage labor",
            "labelBn": "অনিয়মিত/দিনমজুর",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "Seasonal employment",
            "labelBn": "মৌসুমী কর্মসংস্থান",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "5",
            "labelEn": "Others (Specify)",
            "labelBn": "অন্যান্য (নির্দিষ্ট করুন)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        }
    ]
}

WAGE_EMPLOYMENT_STATUS_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in WAGE_EMPLOYMENT_STATUS_CONFIG['options']
    ]



# ==============================================================================
# Unemployed Duration Choices & Config
# ==============================================================================

class UnemployedDurationChoices(models.TextChoices):
    LESS_THAN_1_MONTH = '1', _('Less than 1 month / ১ মাসের কম')
    LESS_THAN_3_MONTHS = '2', _('Less than 3 months / ৩ মাসের কম')
    LESS_THAN_6_MONTHS = '3', _('Less than 6 months / ৬ মাসের কম')
    SIX_MONTHS = '4', _('6 months / ৬ মাস')
    MORE_THAN_6_MONTHS = '5', _('More than 6 months / ৬ মাসের বেশি')


UNEMPLOYED_DURATION_CONFIG = {
    "headerNameEn": "Unemployed Duration (Months)",
    "headerNameBn": "বেকারত্বের সময়কাল (মাস)",
    "placeholderEn": "Select unemployed duration",
    "placeholderBn": "বেকারত্বের সময়কাল নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "Less than 1 month",
            "labelBn": "১ মাসের কম",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Less than 3 months",
            "labelBn": "৩ মাসের কম",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "Less than 6 months",
            "labelBn": "৬ মাসের কম",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "6 months",
            "labelBn": "৬ মাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "5",
            "labelEn": "More than 6 months",
            "labelBn": "৬ মাসের বেশি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        }
    ]
}

UNEMPLOYED_DURATION_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in UNEMPLOYED_DURATION_CONFIG['options']
    ]




# ==============================================================================
# Work Experience Choices & Config
# ==============================================================================

class WorkExperienceChoices(models.TextChoices):
    LESS_THAN_1_YEAR = '1', _('Less than 1 year / ১ বছরের কম')
    ONE_TO_THREE_YEARS = '2', _('1-3 years / ১-৩ বছর')
    THREE_TO_FIVE_YEARS = '3', _('3-5 years / ৩-৫ বছর')
    MORE_THAN_5_YEARS = '4', _('More than 5 years / ৫ বছরের বেশি')


WORK_EXPERIENCE_CONFIG = {
    "headerNameEn": "Work Experience (Years)",
    "headerNameBn": "কাজের অভিজ্ঞতা (বছর)",
    "placeholderEn": "Select work experience",
    "placeholderBn": "কাজের অভিজ্ঞতা নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "Less than 1 year",
            "labelBn": "১ বছরের কম",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "1-3 years",
            "labelBn": "১-৩ বছর",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "3-5 years",
            "labelBn": "৩-৫ বছর",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "More than 5 years",
            "labelBn": "৫ বছরের বেশি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        }
    ]
}

WORK_EXPERIENCE_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in WORK_EXPERIENCE_CONFIG['options']
    ]


# ==============================================================================
# Reason for Leaving Work Choices & Config
# ==============================================================================

class ReasonForLeavingWorkChoices(models.TextChoices):
    LACK_OF_SKILL = '85', _('Lack of skill / দক্ষতার অভাব')
    LACK_OF_CAPITAL = '83', _('Lack of capital/investment / মূলধন/বিনিয়োগের অভাব')
    BUSINESS_LOSS = '84', _('Loss in business / ব্যবসায় ক্ষতি')
    LESS_INCOME = '86', _('Less income / কম আয়')
    NOT_PREFERRED_WORK = '87', _('Not preferred work / পছন্দের কাজ ছিল না')
    LOW_PERFORMANCE = '88', _('Low performance / নিম্ন কর্মক্ষমতা')
    GOT_MARRIED = '89', _('Got married / বিয়ে হয়েছে')
    CHILD_CARING = '90', _('For child caring / সন্তানের যত্নের জন্য')
    HOUSEHOLD_CHORES = '91', _('For household chores / গৃহস্থালী কাজের জন্য')
    OTHERS = '92', _('Others (Specify) / অন্যান্য (উল্লেখ করুন)')


REASON_FOR_LEAVING_WORK_CONFIG = {
    "headerNameEn": "Reason for Leaving Work",
    "headerNameBn": "কর্মত্যাগের কারণ",
    "placeholderEn": "Select reason for leaving work",
    "placeholderBn": "কর্মত্যাগের কারণ নির্বাচন করুন",
    "options": [
        {
            "value": "85",
            "labelEn": "I wasn't capable to manage the employment/business (lack of skill)",
            "labelBn": "আমি চাকরি/ব্যবসাটি পরিচালনা করতে সক্ষম ছিলাম না (দক্ষতার অভাব)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "83",
            "labelEn": "Due to lack of capital/investment",
            "labelBn": "মূলধন/বিনিয়োগের অভাবে",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "84",
            "labelEn": "Due to loss in business",
            "labelBn": "ব্যবসায় ক্ষতির কারণে",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "86",
            "labelEn": "Less income",
            "labelBn": "কম আয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "87",
            "labelEn": "That was not my preferred work",
            "labelBn": "ওটা আমার পছন্দের কাজ ছিল না",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        },
        {
            "value": "88",
            "labelEn": "Low performance",
            "labelBn": "নিম্ন কর্মক্ষমতা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 6,
            "visibleWhen": None
        },
        {
            "value": "89",
            "labelEn": "Got married",
            "labelBn": "বিয়ে হয়েছে",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 7,
            "visibleWhen": None
        },
        {
            "value": "90",
            "labelEn": "For child caring",
            "labelBn": "সন্তানের যত্নের জন্য",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 8,
            "visibleWhen": None
        },
        {
            "value": "91",
            "labelEn": "For household chores",
            "labelBn": "গৃহস্থালী কাজের জন্য",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 9,
            "visibleWhen": None
        },
        {
            "value": "92",
            "labelEn": "Others (Specify)",
            "labelBn": "অন্যান্য (উল্লেখ করুন)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 10,
            "visibleWhen": None
        }
    ]
}

REASON_FOR_LEAVE_CHOICES = [
        (int(opt['value']), opt['labelEn']) 
        for opt in REASON_FOR_LEAVING_WORK_CONFIG['options']
    ]

# ==============================================================================
# Training Project Name Choices & Config
# ==============================================================================

class TrainingProjectNameChoices(models.TextChoices):
    ASSET = '93', _('ASSET / ASSET')
    RAISE = '94', _('RAISE / RAISE')
    STEP = '96', _('STEP / STEP')
    DYD = '203', _('DYD / DYD')
    OTHERS = '97', _('Others (Specify) / অন্যান্য (নির্দিষ্ট করুন)')


TRAINING_PROJECT_NAME_CONFIG = {
    "headerNameEn": "Training Project Name",
    "headerNameBn": "প্রশিক্ষণ প্রকল্পের নাম",
    "placeholderEn": "Select training project name",
    "placeholderBn": "প্রশিক্ষণ প্রকল্পের নাম নির্বাচন করুন",
    "options": [
        {
            "value": "93",
            "labelEn": "ASSET",
            "labelBn": "ASSET",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "94",
            "labelEn": "RAISE",
            "labelBn": "RAISE",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "96",
            "labelEn": "STEP",
            "labelBn": "STEP",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "203",
            "labelEn": "DYD",
            "labelBn": "DYD",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "97",
            "labelEn": "Others (Specify)",
            "labelBn": "অন্যান্য (নির্দিষ্ট করুন)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        }
    ]
}

TRAINING_PROJECT_NAME_CHOICES = [
        (int(opt['value']), opt['labelEn'])
        for opt in TRAINING_PROJECT_NAME_CONFIG['options']
    ]


# ==============================================================================
# Training Attended (Months Ago) Choices & Config
# ==============================================================================

class TrainingMonthsAgoChoices(models.TextChoices):
    LESS_THAN_1_MONTH = '1', _('Less than 1 month / ১ মাসের কম')
    LESS_THAN_3_MONTHS = '2', _('Less than 3 months / ৩ মাসের কম')
    LESS_THAN_6_MONTHS = '3', _('Less than 6 months / ৬ মাসের কম')
    SIX_MONTHS = '4', _('6 months / ৬ মাস')
    MORE_THAN_6_MONTHS = '5', _('More than 6 months / ৬ মাসের বেশি')


TRAINING_MONTHS_AGO_CONFIG = {
    "headerNameEn": "Training Attended (Months Ago)",
    "headerNameBn": "প্রশিক্ষণ নেওয়ার সময় (মাস আগে)",
    "placeholderEn": "Select training attended timeline",
    "placeholderBn": "প্রশিক্ষণ নেওয়ার সময় নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "Less than 1 month",
            "labelBn": "১ মাসের কম",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Less than 3 months",
            "labelBn": "৩ মাসের কম",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "Less than 6 months",
            "labelBn": "৬ মাসের কম",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "6 months",
            "labelBn": "৬ মাস",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "5",
            "labelEn": "More than 6 months",
            "labelBn": "৬ মাসের বেশি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        }
    ]
}

TRAINING_MONTHS_AGO_CHOICES = [
        (int(opt['value']), opt['labelEn'])
        for opt in TRAINING_MONTHS_AGO_CONFIG['options']
    ]

# ==============================================================================
# Computer Skill Level Choices & Config
# ==============================================================================

class ComputerSkillChoices(models.TextChoices):
    NO_SKILL = '1', _('No computer skills at all / কম্পিউটারের কোনো দক্ষতাই নেই')
    BASIC = '2', _('Knows at least MS Word and Internet browsing / অন্তত এমএস ওয়ার্ড ও ইন্টারনেট ব্রাউজিং জানে')
    GOOD = '3', _('Good operating skills / ভালো পরিচালন দক্ষতা')


COMPUTER_SKILL_CONFIG = {
    "headerNameEn": "Computer Skill Level",
    "headerNameBn": "কম্পিউটার দক্ষতা",
    "placeholderEn": "Select computer skill level",
    "placeholderBn": "কম্পিউটার দক্ষতা নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "No computer skills at all",
            "labelBn": "কম্পিউটারের কোনো দক্ষতাই নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Knows at least MS Word and Internet browsing",
            "labelBn": "অন্তত এমএস ওয়ার্ড ও ইন্টারনেট ব্রাউজিং জানে",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "Good operating skills",
            "labelBn": "ভালো পরিচালন দক্ষতা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        }
    ]
}

COMPUTER_SKILL_CHOICES = [
        (int(opt['value']), opt['labelEn'])
        for opt in COMPUTER_SKILL_CONFIG['options']
    ]

# ==============================================================================
# App Usage Choices & Config
# ==============================================================================

class AppUsageChoices(models.TextChoices):
    INTERNET_BROWSER = '1', _('Internet browser / ইন্টারনেট ব্রাউজার')
    YOUTUBE = '2', _('YouTube / ইউটিউব')
    FACEBOOK = '4', _('Facebook / ফেসবুক')
    WHATSAPP = '3', _('WhatsApp / হোয়াটসঅ্যাপ')
    EMAIL = '5', _('Email / ইমেইল')
    IMO = '6', _('Imo / ইমো')


APP_USAGE_CONFIG = {
    "headerNameEn": "App Usage",
    "headerNameBn": "অ্যাপ ব্যবহার",
    "placeholderEn": "Select app usage",
    "placeholderBn": "অ্যাপ ব্যবহার নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "Internet browser",
            "labelBn": "ইন্টারনেট ব্রাউজার",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "YouTube",
            "labelBn": "ইউটিউব",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "Facebook",
            "labelBn": "ফেসবুক",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "WhatsApp",
            "labelBn": "হোয়াটসঅ্যাপ",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "5",
            "labelEn": "Email",
            "labelBn": "ইমেইল",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        },
        {
            "value": "6",
            "labelEn": "Imo",
            "labelBn": "ইমো",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 6,
            "visibleWhen": None
        }
    ]
}

APP_USAGE_CHOICES = [
        (int(opt['value']), opt['labelEn'])
        for opt in APP_USAGE_CONFIG['options']
    ]

# ==============================================================================
# Vehicle Type Choices & Config
# ==============================================================================

class VehicleTypeChoices(models.TextChoices):
    LIGHT = '199', _('Light / হালকা')
    MEDIUM = '200', _('Medium / মাঝারি')
    HEAVY = '201', _('Heavy / ভারী')
    NON_MOTORIZED = '202', _('Non-motorized transport driver (Rickshaw, van etc.) / অযান্ত্রিক পরিবহন চালক (রিকশা, ভ্যান ইত্যাদি)')


VEHICLE_TYPE_CONFIG = {
    "headerNameEn": "Vehicle Type",
    "headerNameBn": "যানবাহনের ধরন",
    "placeholderEn": "Select vehicle type",
    "placeholderBn": "যানবাহনের ধরন নির্বাচন করুন",
    "options": [
        {
            "value": "199",
            "labelEn": "Light",
            "labelBn": "হালকা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "200",
            "labelEn": "Medium",
            "labelBn": "মাঝারি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "201",
            "labelEn": "Heavy",
            "labelBn": "ভারী",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "202",
            "labelEn": "Non-motorized transport driver (Rickshaw, van etc.)",
            "labelBn": "অযান্ত্রিক পরিবহন চালক (রিকশা, ভ্যান ইত্যাদি)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        }
    ]
}

VEHICLE_TYPE_CHOICES = [
        (int(opt['value']), opt['labelEn'])
        for opt in VEHICLE_TYPE_CONFIG['options']
    ]


# ==============================================================================
# Driving Training Location Choices & Config
# ==============================================================================

class DrivingTrainingLocationChoices(models.TextChoices):
    DYD = '1', _('DYD / যুব উন্নয়ন অধিদপ্তর')
    OTHER_GOVT = '2', _('Other govt. organization / অন্যান্য সরকারি প্রতিষ্ঠান')
    NGO = '3', _('NGO / এনজিও')
    PRIVATE = '4', _('Private institution / বেসরকারি প্রতিষ্ঠান')
    OTHER = '5', _('Other (Specify) / অন্যান্য (নির্দিষ্ট করুন)')


DRIVING_TRAINING_LOCATION_CONFIG = {
    "headerNameEn": "Driving Training Location",
    "headerNameBn": "ড্রাইভিং প্রশিক্ষণের স্থান",
    "placeholderEn": "Select driving training location",
    "placeholderBn": "ড্রাইভিং প্রশিক্ষণের স্থান নির্বাচন করুন",
    "options": [
        {
            "value": "1",
            "labelEn": "DYD",
            "labelBn": "যুব উন্নয়ন অধিদপ্তর",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "2",
            "labelEn": "Other govt. organization",
            "labelBn": "অন্যান্য সরকারি প্রতিষ্ঠান",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "3",
            "labelEn": "NGO",
            "labelBn": "এনজিও",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "4",
            "labelEn": "Private institution",
            "labelBn": "বেসরকারি প্রতিষ্ঠান",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "5",
            "labelEn": "Other (Specify)",
            "labelBn": "অন্যান্য (নির্দিষ্ট করুন)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        }
    ]
}

DRIVING_TRAINING_LOCATION_CHOICES = [
        (int(opt['value']), opt['labelEn'])
        for opt in DRIVING_TRAINING_LOCATION_CONFIG['options']
    ]

# ==============================================================================
# Livelihood Plan Choices & Config
# ==============================================================================

class LivelihoodPlanChoices(models.TextChoices):
    GOVT_JOB = '112', _('Govt. job / সরকারী চাকরি')
    PRIVATE_JOB = '113', _('Private job / বেসরকারি চাকরি')
    BUSINESS = '114', _('Business / ব্যবসা')
    GO_ABROAD = '115', _('Go abroad / বিদেশে যাওয়া')
    NO_PLAN = '116', _('No plan yet / এখনো কোনো পরিকল্পনা নেই')


LIVELIHOOD_PLAN_CONFIG = {
    "headerNameEn": "Livelihood Plan",
    "headerNameBn": "জীবিকার পরিকল্পনা",
    "placeholderEn": "Select livelihood plan",
    "placeholderBn": "জীবিকার পরিকল্পনা নির্বাচন করুন",
    "options": [
        {
            "value": "112",
            "labelEn": "I want to work (govt. job)",
            "labelBn": "আমি সরকারী চাকরি করতে চাই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "113",
            "labelEn": "I want to work (private job)",
            "labelBn": "আমি বেসরকারি চাকরি করতে চাই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "114",
            "labelEn": "I want to do business",
            "labelBn": "আমি ব্যবসা করতে চাই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "115",
            "labelEn": "I want to go abroad",
            "labelBn": "আমি বিদেশে যেতে চাই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "116",
            "labelEn": "No plan yet",
            "labelBn": "এখনো কোনো পরিকল্পনা নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        }
    ]
}

LIVELIHOOD_PLAN_CHOICES = [
        (int(opt['value']), opt['labelEn'])
        for opt in LIVELIHOOD_PLAN_CONFIG['options']
    ]


# ==============================================================================
# Employment Challenge Type Choices & Config
# ==============================================================================

class EmploymentChallengeTypeChoices(models.TextChoices):
    LACK_OF_SKILL = '184', _("Don't have skill/knowledge / দক্ষতা/জ্ঞান নেই")
    LACK_OF_CERTIFICATE = '185', _("Don't have certificates / কোনো সার্টিফিকেট নেই")
    FAILED_INTERVIEW = '186', _("Didn't pass job exam/interview / পরীক্ষা/সাক্ষাৎকারে উত্তীর্ণ হতে পারিনি")
    LACK_OF_DEMAND = '187', _("Lack of demand product/service / পণ্য/পরিষেবার চাহিদার অভাব")
    NO_EMPLOYER_RESPONSE = '188', _("Didn't get response from employer / নিয়োগকর্তার কাছ থেকে সাড়া পাওয়া যায়নি")
    LACK_OF_CAPITAL = '189', _("Lack of capital/investment / মূলধন/বিনিয়োগের অভাব")
    SAFETY_CONCERNS = '190', _("Safety/Harassment Concerns / নিরাপত্তা/হয়রানির উদ্বেগ")
    LACK_OF_INTEREST = '191', _("Lack of Interest / আগ্রহের অভাব")
    LACK_OF_CHILDCARE = '192', _("Lack of Childcare Support / শিশু পরিচর্যা সহায়তার অভাব")
    COMMUTE_ISSUES = '193', _("Distance/Commute issues / দূরত্ব/যাতায়াতের সমস্যা")
    LACK_OF_AWARENESS = '194', _("Lack of Awareness about Job Opportunities / সুযোগ সম্পর্কে সচেতনতার অভাব")
    FAMILY_CONSTRAINTS = '195', _("Family constraints / পারিবারিক সীমাবদ্ধতা")
    OTHERS = '196', _("Others (Specify) / অন্যান্য (নির্দিষ্ট করুন)")


EMPLOYMENT_CHALLENGE_TYPE_CONFIG = {
    "headerNameEn": "Employment Challenge Type",
    "headerNameBn": "কর্মসংস্থানে চ্যালেঞ্জের ধরন",
    "placeholderEn": "Select employment challenge type",
    "placeholderBn": "কর্মসংস্থানে চ্যালেঞ্জের ধরন নির্বাচন করুন",
    "options": [
        {
            "value": "184",
            "labelEn": "I don't have skill/knowledge",
            "labelBn": "আমার দক্ষতা/জ্ঞান নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "185",
            "labelEn": "I don't have certificates",
            "labelBn": "আমার কোনো সার্টিফিকেট নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "186",
            "labelEn": "I didn't pass the job exam/interview",
            "labelBn": "আমি চাকরির পরীক্ষা/সাক্ষাৎকারে উত্তীর্ণ হতে পারিনি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "187",
            "labelEn": "Lack of demand product/service",
            "labelBn": "পণ্য/পরিষেবার চাহিদার অভাব",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "188",
            "labelEn": "Didn't get response from employer",
            "labelBn": "নিয়োগকর্তার কাছ থেকে কোনো সাড়া পাওয়া যায়নি",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        },
        {
            "value": "189",
            "labelEn": "Lack of capital/investment",
            "labelBn": "মূলধন/বিনিয়োগের অভাব",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 6,
            "visibleWhen": None
        },
        {
            "value": "190",
            "labelEn": "Safety/Harassment Concerns",
            "labelBn": "নিরাপত্তা/হয়রানির উদ্বেগ",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 7,
            "visibleWhen": None
        },
        {
            "value": "191",
            "labelEn": "Lack of Interest",
            "labelBn": "আগ্রহের অভাব",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 8,
            "visibleWhen": None
        },
        {
            "value": "192",
            "labelEn": "Lack of Childcare Support",
            "labelBn": "শিশু পরিচর্যা সহায়তার অভাব",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 9,
            "visibleWhen": None
        },
        {
            "value": "193",
            "labelEn": "Distance/Commute issues",
            "labelBn": "দূরত্ব/যাতায়াতের সমস্যা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 10,
            "visibleWhen": None
        },
        {
            "value": "194",
            "labelEn": "Lack of Awareness about Job Opportunities",
            "labelBn": "কর্মসংস্থানের সুযোগ সম্পর্কে সচেতনতার অভাব",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 11,
            "visibleWhen": None
        },
        {
            "value": "195",
            "labelEn": "Family constraints (marriage, household chores etc.)",
            "labelBn": "পারিবারিক সীমাবদ্ধতা (বিবাহ, গৃহস্থালীর কাজ ইত্যাদি)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 12,
            "visibleWhen": None
        },
        {
            "value": "196",
            "labelEn": "Others (Specify)",
            "labelBn": "অন্যান্য (নির্দিষ্ট করুন)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 13,
            "visibleWhen": None
        }
    ]
}

EMPLOYMENT_CHALLENGE_TYPE_CHOICES = [
        (int(opt['value']), opt['labelEn'])
        for opt in EMPLOYMENT_CHALLENGE_TYPE_CONFIG['options']
    ]



# ==============================================================================
# Onsite Training Challenge Types Choices & Config
# ==============================================================================

class OnsiteTrainingChallengeTypeChoices(models.TextChoices):
    SAFETY_SECURITY = '138', _('Safety/security / নিরাপত্তা/সুরক্ষা')
    FAMILY_BARRIER = '139', _('Family barrier / পারিবারিক বাধা')
    CHILD_CARE = '140', _('Child care / শিশু যত্ন')
    FINANCIAL_BARRIER = '141', _('Financial barrier / আর্থিক বাধা')
    SOCIAL_BARRIER = '142', _('Social barrier / সামাজিক বাধা')
    OTHERS = '143', _('Others (Specify) / অন্যান্য (নির্দিষ্ট করুন)')


ONSITE_TRAINING_CHALLENGE_TYPE_CONFIG = {
    "headerNameEn": "Onsite Training Challenge Types",
    "headerNameBn": "সরাসরি প্রশিক্ষণে চ্যালেঞ্জের ধরন",
    "placeholderEn": "Select onsite training challenges",
    "placeholderBn": "সরাসরি প্রশিক্ষণে চ্যালেঞ্জের ধরন নির্বাচন করুন",
    "options": [
        {
            "value": "138",
            "labelEn": "Safety/security",
            "labelBn": "নিরাপত্তা/সুরক্ষা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "139",
            "labelEn": "Family barrier",
            "labelBn": "পারিবারিক বাধা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "140",
            "labelEn": "Child care",
            "labelBn": "শিশু যত্ন",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "141",
            "labelEn": "Financial barrier",
            "labelBn": "আর্থিক বাধা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        },
        {
            "value": "142",
            "labelEn": "Social barrier",
            "labelBn": "সামাজিক বাধা",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 5,
            "visibleWhen": None
        },
        {
            "value": "143",
            "labelEn": "Others (Specify)",
            "labelBn": "অন্যান্য (নির্দিষ্ট করুন)",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 6,
            "visibleWhen": None
        }
    ]
}


ONSITE_TRAINING_CHALLENGE_TYPE_CHOICES = [
        (int(opt['value']), opt['labelEn'])
        for opt in ONSITE_TRAINING_CHALLENGE_TYPE_CONFIG['options']
    ]


# ==============================================================================
# Difficulty Seeing Choices & Config
# ==============================================================================
class DifficultySeeingChoices(models.TextChoices):
    NO_DIFFICULTY = '180', _('No difficulty / কোনো অসুবিধা নেই')
    SOME_DIFFICULTY = '181', _('Some difficulty / কিছু অসুবিধা হয়')
    A_LOT_OF_DIFFICULTY = '182', _('A lot of difficulty / অনেক অসুবিধা হয়')
    CANNOT_SEE = '183', _('Cannot see at all / একদমই দেখি না')


DIFFICULTY_SEEING_CONFIG = {
    "headerNameEn": "Difficulty Seeing",
    "headerNameBn": "দেখতে অসুবিধা",
    "placeholderEn": "Select seeing difficulty level",
    "placeholderBn": "দেখতে অসুবিধার মাত্রা নির্বাচন করুন",
    "options": [
        {
            "value": "180",
            "labelEn": "No difficulty",
            "labelBn": "কোনো অসুবিধা নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "181",
            "labelEn": "Some difficulty",
            "labelBn": "কিছু অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "182",
            "labelEn": "A lot of difficulty",
            "labelBn": "অনেক অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "183",
            "labelEn": "Cannot see at all",
            "labelBn": "একদমই দেখি না",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        }
    ]
}

DIFFICULTY_SEEING_CHOICES = [
    (int(opt['value']), opt['labelEn']) 
        for opt in DIFFICULTY_SEEING_CONFIG['options']
    ]

# ==============================================================================
# Difficulty Hearing Choices & Config
# ==============================================================================

class DifficultyHearingChoices(models.TextChoices):
    NO_DIFFICULTY = '180', _('No difficulty / কোনো অসুবিধা নেই')
    SOME_DIFFICULTY = '181', _('Some difficulty / কিছু অসুবিধা হয়')
    A_LOT_OF_DIFFICULTY = '182', _('A lot of difficulty / অনেক অসুবিধা হয়')
    CANNOT_HEAR = '183', _('Cannot hear at all / একদমই শুনি না')


DIFFICULTY_HEARING_CONFIG = {
    "headerNameEn": "Difficulty Hearing",
    "headerNameBn": "শুনতে অসুবিধা",
    "placeholderEn": "Select hearing difficulty level",
    "placeholderBn": "শুনতে অসুবিধার মাত্রা নির্বাচন করুন",
    "options": [
        {
            "value": "180",
            "labelEn": "No difficulty",
            "labelBn": "কোনো অসুবিধা নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "181",
            "labelEn": "Some difficulty",
            "labelBn": "কিছু অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "182",
            "labelEn": "A lot of difficulty",
            "labelBn": "অনেক অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "183",
            "labelEn": "Cannot hear at all",
            "labelBn": "একদমই শুনি না",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        }
    ]
}

DIFFICULTY_HEARING_CHOICES = [
    (int(opt['value']), opt['labelEn']) 
        for opt in DIFFICULTY_HEARING_CONFIG['options']
    ]


# ==============================================================================
# Difficulty Walking Choices & Config
# ==============================================================================

class DifficultyWalkingChoices(models.TextChoices):
    NO_DIFFICULTY = '180', _('No difficulty / কোনো অসুবিধা নেই')
    SOME_DIFFICULTY = '181', _('Some difficulty / কিছু অসুবিধা হয়')
    A_LOT_OF_DIFFICULTY = '182', _('A lot of difficulty / অনেক অসুবিধা হয়')
    CANNOT_WALK = '183', _('Cannot walk at all / একদমই চলি না')


DIFFICULTY_WALKING_CONFIG = {
    "headerNameEn": "Difficulty Walking",
    "headerNameBn": "হাঁটতে অসুবিধা",
    "placeholderEn": "Select walking difficulty level",
    "placeholderBn": "হাঁটতে অসুবিধার মাত্রা নির্বাচন করুন",
    "options": [
        {
            "value": "180",
            "labelEn": "No difficulty",
            "labelBn": "কোনো অসুবিধা নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "181",
            "labelEn": "Some difficulty",
            "labelBn": "কিছু অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "182",
            "labelEn": "A lot of difficulty",
            "labelBn": "অনেক অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "183",
            "labelEn": "Cannot walk at all",
            "labelBn": "একদমই হাঁটতে পারি না",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        }
    ]
}

DIFFICULTY_WALKING_CHOICES = [
    (int(opt['value']), opt['labelEn']) 
        for opt in DIFFICULTY_WALKING_CONFIG['options']
    ]


# ==============================================================================
# Difficulty Remembering Choices & Config
# ==============================================================================

class DifficultyRememberingChoices(models.TextChoices):
    NO_DIFFICULTY = '180', _('No difficulty / কোনো অসুবিধা নেই')
    SOME_DIFFICULTY = '181', _('Some difficulty / কিছু অসুবিধা হয়')
    A_LOT_OF_DIFFICULTY = '182', _('A lot of difficulty / অনেক অসুবিধা হয়')
    CANNOT_REMEMBER = '183', _('Cannot remember at all / একদমই মনে রাখতে পারি না')


DIFFICULTY_REMEMBERING_CONFIG = {
    "headerNameEn": "Difficulty Remembering",
    "headerNameBn": "মনে রাখতে অসুবিধা",
    "placeholderEn": "Select remembering difficulty level",
    "placeholderBn": "মনে রাখতে অসুবিধার মাত্রা নির্বাচন করুন",
    "options": [
        {
            "value": "180",
            "labelEn": "No difficulty",
            "labelBn": "কোনো অসুবিধা নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "181",
            "labelEn": "Some difficulty",
            "labelBn": "কিছু অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "182",
            "labelEn": "A lot of difficulty",
            "labelBn": "অনেক অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "183",
            "labelEn": "Cannot remember at all",
            "labelBn": "একদমই মনে রাখতে পারি না",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        }
    ]
}

DIFFICULTY_REMEMBERING_CHOICES = [
    (int(opt['value']), opt['labelEn']) 
        for opt in DIFFICULTY_REMEMBERING_CONFIG['options']
    ]


# ==============================================================================
# Difficulty Selfcare Choices & Config
# ==============================================================================


class DifficultySelfcareChoices(models.TextChoices):
    NO_DIFFICULTY = '180', _('No difficulty / কোনো অসুবিধা নেই')
    SOME_DIFFICULTY = '181', _('Some difficulty / কিছু অসুবিধা হয়')
    A_LOT_OF_DIFFICULTY = '182', _('A lot of difficulty / অনেক অসুবিধা হয়')
    CANNOT_REMEMBER = '183', _('Cannot selfcare at all / একদমই নিজের যত্ন নিতে পারি না')


DIFFICULTY_SELFCARE_CONFIG = {
    "headerNameEn": "Difficulty Selfcare",
    "headerNameBn": "নিজের যত্নে অসুবিধা",
    "placeholderEn": "Select selfcare difficulty level",
    "placeholderBn": "নিজেকে যত্ন দেওয়ার অসুবিধার মাত্রা নির্বাচন করুন",
    "options": [
        {
            "value": "180",
            "labelEn": "No difficulty",
            "labelBn": "কোনো অসুবিধা নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "181",
            "labelEn": "Some difficulty",
            "labelBn": "কিছু অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "182",
            "labelEn": "A lot of difficulty",
            "labelBn": "অনেক অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "183",
            "labelEn": "Cannot selfcare at all",
            "labelBn": "একদমই নিজের যত্ন নিতে পারি না",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        }
    ]
}


DIFFICULTY_SELFCARE_CHOICES = [
    (int(opt['value']), opt['labelEn']) 
        for opt in DIFFICULTY_SELFCARE_CONFIG['options']
    ]

# ==============================================================================
# Difficulty Communicating Choices & Config
# ==============================================================================

class DifficultyCommunicatingChoices(models.TextChoices):
    NO_DIFFICULTY = '180', _('No difficulty / কোনো অসুবিধা নেই')
    SOME_DIFFICULTY = '181', _('Some difficulty / কিছু অসুবিধা হয়')
    A_LOT_OF_DIFFICULTY = '182', _('A lot of difficulty / অনেক অসুবিধা হয়')
    CANNOT_REMEMBER = '183', _('Cannot remember at all / একদমই মনে রাখতে পারি না')


DIFFICULTY_COMMUNICATING_CONFIG = {
    "headerNameEn": "Difficulty Communicating",
    "headerNameBn": "যোগাযোগে অসুবিধা",
    "placeholderEn": "Select communicating difficulty level",
    "placeholderBn": "যোগাযোগে অসুবিধা মাত্রা নির্বাচন করুন",
    "options": [
        {
            "value": "180",
            "labelEn": "No difficulty",
            "labelBn": "কোনো অসুবিধা নেই",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 1,
            "visibleWhen": None
        },
        {
            "value": "181",
            "labelEn": "Some difficulty",
            "labelBn": "কিছু অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 2,
            "visibleWhen": None
        },
        {
            "value": "182",
            "labelEn": "A lot of difficulty",
            "labelBn": "অনেক অসুবিধা হয়",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 3,
            "visibleWhen": None
        },
        {
            "value": "183",
            "labelEn": "Cannot communicate at all",
            "labelBn": "একদমই যোগাযোগ করতে পারি না",
            "status": 1,
            "score": 0,
            "colorHex": None,
            "displayOrder": 4,
            "visibleWhen": None
        }
    ]
}

DIFFICULTY_COMMUNICATING_CHOICES = [
    (int(opt['value']), opt['labelEn']) 
        for opt in DIFFICULTY_COMMUNICATING_CONFIG['options']
    ]