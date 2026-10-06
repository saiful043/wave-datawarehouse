import uuid
import re
from datetime import datetime, date
import pandas as pd
from django.db import transaction
from apps.projects.models import Project

from apps.beneficiaries.models import BeneficiaryInfo, BeneficiaryGeoLocation, BeneficiaryAttachment,BeneficiaryHouseHoldInfo, BeneficiaryDifficulty, BeneficiaryEducationInfo,BeneficiaryEmploymentInfo, BeneficiaryDigitalSkill, BeneficiaryWillingnessInfo
from apps.core.models import Location, Gender, IndigenousGroupType, Package
from apps.core.constants import (RELATION_TO_HH_HEAD_CONFIG, HHCountUncollectedReasonChoices,
DIFFICULTY_SEEING_CHOICES, DIFFICULTY_HEARING_CHOICES,
    DIFFICULTY_WALKING_CHOICES, DIFFICULTY_REMEMBERING_CHOICES,
    DIFFICULTY_SELFCARE_CHOICES, DIFFICULTY_COMMUNICATING_CHOICES, 
    HIGHEST_EDUCATION_LEVEL_CONFIG_CHOICES, INSTITUTION_TYPE_CHOICES,
    MADRASHA_TYPE_CHOICES,DISCONTINUE_REASON_CHOICES, EMPLOYMENT_STATUS_CHOICES, SELF_EMPLOYMENT_TYPE_CHOICES, WAGE_EMPLOYMENT_STATUS_CHOICES,
    UNEMPLOYED_DURATION_CHOICES, WORK_EXPERIENCE_CHOICES, REASON_FOR_LEAVE_CHOICES, TRAINING_PROJECT_NAME_CHOICES, TRAINING_MONTHS_AGO_CHOICES,
    COMPUTER_SKILL_CHOICES, VEHICLE_TYPE_CHOICES, DRIVING_TRAINING_LOCATION_CHOICES, APP_USAGE_CHOICES, LIVELIHOOD_PLAN_CHOICES, EMPLOYMENT_CHALLENGE_TYPE_CHOICES, ONSITE_TRAINING_CHALLENGE_TYPE_CHOICES
    )

 # 🎯 config থেকে বৈধ কোডগুলো একবার বের করে সেট বানিয়ে রাখা
_VALID_RELATION_CODES = {
    int(opt["value"]) for opt in RELATION_TO_HH_HEAD_CONFIG["options"]
}

class BeneficiaryETLService:
    def __init__(self, file_path, project_id, package_id, batch_size=5000, celery_task=None):
        self.file_path = file_path
        self.project_id = project_id
        self.package_id = package_id
        self.batch_size = batch_size
        self.celery_task = celery_task

    def run(self):
        project_instance = Project.objects.get(pk=self.project_id)
        package_instance = Package.objects.get(pk=self.package_id)

        location_map = {str(loc.location_id): loc for loc in Location.objects.all()}
        gender_map = {str(g.id): g for g in Gender.objects.all()}
        indigenous_group_map = {str(ig.id): ig for ig in IndigenousGroupType.objects.all()}

        if self.file_path.endswith('.csv'):
            chunks = pd.read_csv(self.file_path, dtype=str, chunksize=self.batch_size)
        else:
            full_df = pd.read_excel(self.file_path, dtype=str)
            chunks = [full_df.iloc[i:i + self.batch_size] for i in range(0, len(full_df), self.batch_size)]

        total_success = 0
        total_rows = 0

        # Parent Model Update Fields
        parent_update_fields = [
            'projects_project','package', 'applicant_name_en', 'applicant_name_bn',
            'no_nid_declaration', 'applicant_nid', 'applicant_brn', 'applicant_dob',
            'applicant_age', 'applicant_gender', 'mobile_owner', 'mobile_self',
            'mobile_request', 'relation_to_hh_head', 'relation_to_hh_head_others',
            'marital_status', 'has_children', 'children_count',
            'has_dependent_children', 'has_childcare_support', 'data_collection_date',
            'comments_of_enumerator'
        ]

        for df_chunk in chunks:
            beneficiary_objs = []
            response_ids = []

            total_rows += len(df_chunk)

            with transaction.atomic():
                for idx, row in df_chunk.iterrows():
                    res_id = self._clean_str(row.get('a. রেসপন্স আইডি')) or str(uuid.uuid4())
                    response_ids.append(res_id)

                    dob_val = self._parse_date(row.get('24. উত্তরদাতার জন্ম তারিখ (এনআইডি/জন্ম নিবন্ধন অনুসারে)'))
                    data_date = self._parse_date(row.get('b. তথ্য সংগ্রহের তারিখ'))
                    gender_id = self._clean_str(row.get('26. উত্তরদাতার লিঙ্গ'))
                    calculated_age = self._calculate_age(dob_val, data_date)

                    b_obj = BeneficiaryInfo(
                        response_id=res_id,
                        projects_project=project_instance,
                        package = package_instance,
                        applicant_name_en=self._clean_str(row.get('22. সম্ভাব্য উপকারভোগীর/উত্তরদাতার নাম (ইংরেজিতে)')),
                        applicant_name_bn=self._clean_str(row.get('22. সম্ভাব্য উপকারভোগীর/উত্তরদাতার নাম (বাংলায়)')),
                        no_nid_declaration=self._parse_bool(row.get('23. উত্তরদাতার এনআইডি নাকি জন্ম নিবন্ধন')),
                        applicant_nid=self._clean_nid_or_brn(row.get('23.1 উত্তরদাতার এনআইডি নম্বর')),
                        applicant_brn=self._clean_nid_or_brn(row.get('23.2 উত্তরদাতার জন্ম নিবন্ধন নম্বর')),
                        applicant_dob=dob_val,
                        applicant_age=calculated_age,
                        applicant_gender=gender_map.get(gender_id),
                        mobile_owner=self._clean_str(row.get('25. উত্তরদাতার মোবাইল নম্বর')),
                        mobile_self=self._clean_phone(row.get('25.1 উত্তরদাতার মোবাইল নম্বর (নিজস্ব)')),
                        mobile_request=self._clean_phone(row.get('25.2 উত্তরদাতার মোবাইল নম্বর (বিকল্প)')),
                        relation_to_hh_head=self._parse_relation_to_hh_head(row.get('27. খানা প্রধান আপনার কি হয়?')),
                        relation_to_hh_head_others=self._clean_str(row.get('27. অন্যান্য হলে সম্পর্ক উল্লেখ করুন')),
                        marital_status=self._parse_int(row.get('28. উত্তরদাতার বৈবাহিক অবস্থা')),
                        has_children=self._parse_bool(row.get('29. আপনার কি কোনো সন্তান আছে?')),
                        children_count=self._parse_int(row.get('30. যদি থাকে, তবে কতজন?')),
                        has_dependent_children=self._parse_bool(row.get('31. আপনার কি এমন কোনো সন্তান আছে যে আপনার ওপর নির্ভরশীল (৬ বছর বয়স পর্যন্ত)?')),
                        has_childcare_support=self._parse_bool(row.get('32. আপনার বাড়িতে কি এমন কেউ আছেন যিনি আপনার সন্তানের যত্ন নিতে পারেন?')),
                        data_collection_date=data_date,
                        comments_of_enumerator=self._clean_str(row.get('86. জরিপকারীর মন্তব্য'))
                    )
                    beneficiary_objs.append((b_obj, row))

                # 🎯 1. Upsert Parent Model (BeneficiaryInfo)
                BeneficiaryInfo.objects.bulk_create(
                    [item[0] for item in beneficiary_objs],
                    update_conflicts=True,
                    unique_fields=['response_id'],
                    update_fields=parent_update_fields
                )

                # 🎯 2. Primary Key ম্যাপ পেতে DB থেকে ফেচ করা
                existing_beneficiaries = BeneficiaryInfo.objects.filter(
                    response_id__in=response_ids
                ).in_bulk(field_name='response_id')

                geo_objs = []
                attachment_objs = []
                household_objs = []
                difficulty_objs = []
                education_objs = []
                employment_objs = []
                digital_skill_objs = []
                willingness_objs = []

                # 🎯 3. চাইল্ড অবজেক্ট প্রস্তুত করা
                for b_obj, row in beneficiary_objs:
                    b_instance = existing_beneficiaries.get(b_obj.response_id)
                    if not b_instance:
                        continue

                    geo_objs.append(
                        BeneficiaryGeoLocation(
                            beneficiary=b_instance,
                            division=location_map.get(self._clean_str(row.get('1. বিভাগ'))),
                            district=location_map.get(self._clean_str(row.get('2. জেলা'))),
                            upazila=location_map.get(self._clean_str(row.get('3. উপজেলা'))),
                            pouroword_or_union=self._parse_int(row.get('4. পৌরওয়ার্ড নাকি ইউনিয়ন')),
                            union=location_map.get(self._clean_str(row.get('5. ইউনিয়ন'))),
                            ward_no=self._clean_str(row.get('6. ওয়ার্ড নম্বর')),
                            village=location_map.get(self._clean_str(row.get('7.1 গ্রাম/মহল্লা'))),
                            village_other=self._clean_str(row.get('7.2 গ্রাম/মহল্লা — তালিকায় না থাকলে')),
                            household_identification=self._clean_str(row.get('8. অবস্থান/খানা শনাক্তকরণ')),
                            latitude=row.get('9. জিপিএস অক্ষাংশ (° N)') if pd.notna(row.get('9. জিপিএস অক্ষাংশ (° N)')) else None,
                            longitude=row.get('9. জিপিএস দ্রাঘিমাংশ (° E)') if pd.notna(row.get('9. জিপিএস দ্রাঘিমাংশ (° E)')) else None,
                        )
                    )

                    attachment_objs.append(
                        BeneficiaryAttachment(
                            beneficiary=b_instance,
                            attachment_photo=self._parse_bool(row.get('85.1 আবেদনকারীর ছবি')),
                            attachment_nid_doc=self._parse_bool(row.get('85.2 আবেদনকারীর এনআইডি')),
                            attachment_brn_doc=self._parse_bool(row.get('85.3 জন্ম নিবন্ধন সনদ')),
                            attachment_hh_head_nid_doc=self._parse_bool(row.get('85.4 পরিবার প্রধানের এনআইডি')),
                            attachment_testimonial_or_certificate=self._parse_bool(row.get('85. সনদ নাকি প্রশংসাপত্র')),
                            education_certificate=self._clean_str(row.get('85.5 সর্বোচ্চ শিক্ষার সনদ')),
                            testimonial=self._clean_str(row.get('85.6 প্রশংসাপত্র')),
                            training_certificate=self._clean_str(row.get('85.7 প্রশিক্ষণ সনদ')),
                        )
                    )

                    hh_gender_id = self._clean_str(row.get('11. খানা প্রধানের লিঙ্গ'))
                    household_objs.append(
                        BeneficiaryHouseHoldInfo(
                            beneficiary=b_instance,
                            hh_head_name_en=self._clean_str(row.get('10. খানা প্রধানের নাম (ইংরেজিতে)')),
                            hh_head_name_bn=self._clean_str(row.get('10. খানা প্রধানের নাম (বাংলায়)')),
                            hh_head_gender=gender_map.get(hh_gender_id),
                            hh_head_nid=self._clean_nid_or_brn(row.get('12. খানা প্রধানের এনআইডি নম্বর')),
                            hh_total_members=self._parse_int(row.get('13. আপনার খানায় কতজন সদস্য আছেন?')),
                            hh_count_1535=self._parse_int(row.get('14. এই খানায় ১৫-৩৫ বছর বয়সী কতজন সদস্য আছেন?')),
                            hh_count_1535_collected=self._parse_int(row.get('15. ১৫ থেকে ৩৫ বছর বয়সী কতজন সদস্যের তথ্য সংগ্রহ করা সম্ভব?')),
                            hh_count_1535_uncollected_reason=self._parse_multi_choice_text(row.get('16. যাদের ক্ষেত্রে তথ্য সংগ্রহ করা সম্ভব নয়, অনুগ্রহ করে তার কারণ উল্লেখ করুন।')),
                            hh_count_earning=self._parse_int(row.get('17. এই খানায় কতজন উপার্জনকারী সদস্য আছেন?')),
                            is_indigenous=self._parse_bool(row.get('18. আপনার খানাটি কি ক্ষুদ্র নৃ-গোষ্ঠীর অংশ?')),
                            indigenous_group_type=indigenous_group_map.get(self._clean_str(row.get('19. যদি হ্যাঁ হয়, তাহলে কোনটি?'))),
                            indigenous_group_others=self._clean_str(row.get('19. অন্যান্য হলে নৃগোষ্ঠীর নাম উল্লেখ করুন')),
                            household_special_area=self._parse_int(row.get('20. এই পরিবারটি কি এর মধ্যে কোনো এলাকার অন্তর্ভুক্ত?')),
                            household_special_area_specify=self._clean_str(row.get('21. অনুগ্রহ করে সংশ্লিষ্ট চা-বাগান/হাওর/চর/পার্বত্য এলাকা/উপকূলীয় এলাকার নাম উল্লেখ করুন')),
                        )
                    )

                    difficulty_objs.append(
                        BeneficiaryDifficulty(
                            beneficiary=b_instance,
                            seeing=self._parse_disability_choice(row.get('33. চশমা পরার পরেও কি আপনার দেখতে অসুবিধা হয়?'), DIFFICULTY_SEEING_CHOICES),
                            hearing=self._parse_disability_choice(row.get('34. হিয়ারিং এইড ব্যবহার করা সত্ত্বেও আপনার কি শুনতে অসুবিধা হয়?'), DIFFICULTY_HEARING_CHOICES),
                            walking=self._parse_disability_choice(row.get('35. আপনার কি হাঁটতে বা সিঁড়ি বেয়ে উঠতে অসুবিধা হয়?'), DIFFICULTY_WALKING_CHOICES),
                            remembering=self._parse_disability_choice(row.get('36. আপনার কি মনে রাখতে বা মনোযোগ দিতে অসুবিধা হয়?'), DIFFICULTY_REMEMBERING_CHOICES),
                            selfcare=self._parse_disability_choice(row.get('37. আপনার কি নিজের যত্ন নিতে, যেমন সারা শরীর ধোয়া বা পোশাক পরতে অসুবিধা হয়?'), DIFFICULTY_SELFCARE_CHOICES),
                            communicating=self._parse_disability_choice(row.get('38. আপনার স্বাভাবিক ভাষায় যোগাযোগ করতে, যেমন বুঝতে বা বোঝাতে, আপনার কি কোনো অসুবিধা হয়?'), DIFFICULTY_COMMUNICATING_CHOICES),
                            is_pwd=self._parse_bool(row.get('বিশেষ চাহিদা সম্পন্ন ব্যক্তি (PWD)'))
                        )
                    )

                    education_objs.append(
                        BeneficiaryEducationInfo(
                            beneficiary=b_instance,
                            currently_in_education=self._parse_bool(row.get('39. আপনি কি বর্তমানে পড়ালেখার সাথে যুক্ত আছেন?')),
                            highest_education_level=self._parse_int(row.get('40. আপনার শিক্ষাগত যোগ্যতার সর্বোচ্চ স্তর বা ডিগ্রি কী?'), HIGHEST_EDUCATION_LEVEL_CONFIG_CHOICES),
                            other_education_level=self._clean_str(row.get('40. অন্যান্য হলে শিক্ষাগত স্তর লিখুন')),
                            institution_type=self._parse_int(row.get('41. আপনার সর্বোচ্চ ডিগ্রির প্রাতিষ্ঠানিক ধরন কী?'), INSTITUTION_TYPE_CHOICES),
                            madrasha_type=self._parse_int(row.get('42. মাদ্রাসা হলে, কোন ধরনের?'), MADRASHA_TYPE_CHOICES),
                            attended_classes_last_6_months=self._parse_bool(row.get('43. আপনি কি গত ৬ মাসে ক্লাসে উপস্থিত ছিলেন বা পরীক্ষায় অংশ নিয়েছিলেন?')),
                            ever_dropped_out=self._parse_bool(row.get('44. যদি বর্তমানে অধ্যয়নরত না থাকেন: আপনি কি কখনও কাঙ্ক্ষিত স্তর সম্পন্ন করার আগে পড়াশোনা ছেড়ে দিয়েছিলেন?')),
                            discontinue_reason=self._parse_multi_choice_text(row.get('45. পড়াশোনায় বিরতি থাকলে তার কারণ কী?')),
                            discontinue_reason_others=self._clean_str(row.get('45. অন্যান্য হলে বিস্তারিত কারণ লিখুন')),
                            attended_govt_job_exam_last_6_months=self._parse_bool(row.get('46. আপনি কি গত ছয় মাসের মধ্যে কোনো চাকরির পরীক্ষায় অংশ নিয়েছেন / আপনি কি চাকরির পরীক্ষার প্রস্তুতি নিচ্ছেন?')),
                            can_read_bangla=self._parse_bool(row.get('47. আপনি কি বাংলা পড়তে পারেন?')),
                            can_write_bangla=self._parse_bool(row.get('48. আপনি কি বাংলা লিখতে পারেন?')),
                            can_read_english=self._parse_bool(row.get('49. আপনি কি ইংরেজি পড়তে পারেন?')),
                            can_write_english=self._parse_bool(row.get('50. আপনি কি ইংরেজি লিখতে পারেন?'))
                        )
                    )

                    employment_objs.append(
                        BeneficiaryEmploymentInfo(
                            beneficiary=b_instance,
                            is_currently_employed=self._parse_bool(row.get('51. আপনি কি বর্তমানে কোনো আয়-উপার্জনকারী কাজে যুক্ত আছেন?')),
                            employment_status_self_or_wage=self._parse_int(row.get('52. কি ধরনের কর্মসংস্থান?'), EMPLOYMENT_STATUS_CHOICES),
                            current_employment_type=self._parse_int(row.get('53. কোন ধরনের কাজ?'), SELF_EMPLOYMENT_TYPE_CHOICES),
                            wage_employment_status=self._parse_int(row.get('54. আপনার বর্তমান কর্মসংস্থানের অবস্থা কী?'), WAGE_EMPLOYMENT_STATUS_CHOICES),
                            employment_status_others=self._clean_str(row.get('54. অন্যান্য হলে বর্তমান কর্মসংস্থানের অবস্থা উল্লেখ করুন')),
                            income_last_month=self._parse_float(row.get('55. গত মাসে আপনার আয় কত ছিল? (টাকা)')),
                            avg_income_6months=self._parse_float(row.get('56. গত ছয় মাসে আপনার গড় মাসিক আয় কত ছিল? (টাকা)')),
                            unemployment_months=self._parse_int(row.get('57. আপনি কতদিন ধরে বেকার আছেন? (মাস)'), UNEMPLOYED_DURATION_CHOICES),
                            has_work_experience=self._parse_bool(row.get('58. আপনার কি কোনো আয়-উপার্জনকারী কাজের অভিজ্ঞতা আছে?')),
                            experience_years=self._parse_int(row.get('59. যদি হ্যাঁ হয়, তবে আপনার কত বছরের অভিজ্ঞতা আছে? (বছর)'), WORK_EXPERIENCE_CHOICES),
                            left_work_reason=self._parse_int(row.get('60. যদি হ্যাঁ হয়, তবে আপনি সেই কাজটি কেন ছেড়েছিলেন?'), REASON_FOR_LEAVE_CHOICES),
                            left_work_reason_others=self._clean_str(row.get('60. অন্যান্য হলে কর্মত্যাগের কারণ লিখুন')),
                            currently_in_training=self._parse_bool(row.get('61. আপনি কি বর্তমানে কোনো প্রশিক্ষণে (দক্ষতা উন্নয়ন/ভোকেশনাল) যুক্ত আছেন?')),
                            received_skill_training_go_ngo=self._parse_bool(row.get('62. আপনি কি সরকারি প্রকল্প বা অন্য কোনো সংস্থা থেকে দক্ষতা উন্নয়ন বা ভোকেশনাল প্রশিক্ষণ গ্রহণ করেছেন?')),
                            has_vocational_certificate=self._parse_bool(row.get('63. আপনি কি সেই প্রশিক্ষণের সার্টিফিকেট পেয়েছেন?')),
                            training_project_name=self._parse_int(row.get('64. যদি হ্যাঁ হয়, তাহলে প্রকল্প/কর্মসূচির নাম উল্লেখ করুন (একাধিক প্রশিক্ষণ গ্রহণ করা হলে সর্বশেষটি বিবেচনা করুন)'), TRAINING_PROJECT_NAME_CHOICES),
                            training_project_name_others=self._clean_str(row.get('64. অন্যান্য হলে প্রকল্প/প্রোগ্রামের নাম লিখুন')),
                            training_months_ago=self._parse_int(row.get('65. আপনি কত মাস আগে এই প্রশিক্ষণে অংশগ্রহণ করেছিলেন? (মাস)'), TRAINING_MONTHS_AGO_CHOICES),
                            training_trade=self._parse_multi_choice_text(row.get('66. অনুগ্রহ করে আপনার প্রশিক্ষণের ট্রেডের নাম উল্লেখ করুন।')),
                            is_potential_beneficiary=self._parse_bool(row.get('সম্ভাব্য উপকারভোগী'))
                        )
                    )

                    digital_skill_objs.append(
                        BeneficiaryDigitalSkill(
                            beneficiary=b_instance,
                            has_smartphone=self._parse_bool(row.get('67. আপনার কি নিজের স্মার্টফোন আছে?')),
                            has_computer_or_laptop=self._parse_bool(row.get('68. আপনার কি কম্পিউটার/ল্যাপটপ আছে?')),
                            computer_skill=self._parse_int(row.get('69. কম্পিউটার চালনায় আপনার দক্ষতা কেমন?'), COMPUTER_SKILL_CHOICES),
                            uses_internet=self._parse_bool(row.get('70. আপনি কি ইন্টারনেট ব্যবহার করেন?')),
                            app_usage=self._parse_multi_choice_text(row.get('71. আপনি কি এই অ্যাপগুলো ব্যবহার করেন?')),
                            knows_driving=self._parse_bool(row.get('72. আপনি কি গাড়ি চালানো জানেন?')),
                            vehicle_type=self._parse_int(row.get('73. যদি হ্যাঁ হয়, তাহলে কোন ধরনের যানবাহন?'), VEHICLE_TYPE_CHOICES),
                            has_driving_licence=self._parse_bool(row.get('74. আপনার কি ড্রাইভিং লাইসেন্স আছে?')),
                            received_driving_training=self._parse_bool(row.get('75. আপনি কি কখনও কোনো ড্রাইভিং প্রশিক্ষণ নিয়েছেন?')),
                            driving_training_location=self._parse_int(row.get('76. আপনি কোথা থেকে প্রশিক্ষণ নিয়েছেন?'), DRIVING_TRAINING_LOCATION_CHOICES),
                            driving_training_location_others=self._clean_str(row.get('76. অন্যান্য হলে প্রশিক্ষণের স্থান উল্লেখ করুন'))
                        )
                    )

                    willingness_objs.append(
                        BeneficiaryWillingnessInfo(
                            beneficiary=b_instance,
                            livelihood_plan=self._parse_int(row.get('77. জীবিকা নিয়ে এখন আপনার পরিকল্পনা কী?'), LIVELIHOOD_PLAN_CHOICES),
                            searching_employment=self._parse_bool(row.get('78. আপনি কি বর্তমানে কোনো কর্মসংস্থান বা ব্যবসার সুযোগ খুঁজছেন?')),
                            has_employment_challenges=self._parse_bool(row.get('79. আপনি কি চাকরি বা ব্যবসায় যুক্ত হতে কোনো বাধার সম্মুখীন হচ্ছেন?')),
                            employment_challenge_type=self._parse_multi_choice_text(row.get('80. যদি হ্যাঁ হয়, তাহলে সেগুলো কী কী?')),
                            employment_challenge_others=self._clean_str(row.get('80. অন্যান্য চ্যালেঞ্জ লিখুন')),
                            interested_in_training=self._parse_bool(row.get('81. আপনি কি আপনার কর্মসংস্থান তৈরির জন্য কোনো আনুষ্ঠানিক প্রশিক্ষণে অংশ নিতে আগ্রহী?')),
                            has_onsite_training_challenges=self._parse_bool(row.get('82. আপনার এলাকায় সরাসরি প্রশিক্ষণে অংশগ্রহণ করতে কি কোনো অসুবিধা আছে?')),
                            onsite_training_challenge_types=self._parse_multi_choice_text(row.get('83. যদি হ্যাঁ হয়, তাহলে সেগুলো কী কী?')),
                            onsite_training_challenge_others=self._clean_str(row.get('83. অন্যান্য চ্যালেঞ্জ লিখুন')),
                            comfortable_online_training=self._parse_bool(row.get('84. আপনি কি অনলাইন প্রশিক্ষণে অংশগ্রহণ করতে স্বাচ্ছন্দ্যবোধ করেন?'))
                        )
                    )

                # 🎯 4. চাইল্ড মডেলগুলোতে Upsert চালানো (No Delete Needed)
                BeneficiaryGeoLocation.objects.bulk_create(
                    geo_objs,
                    update_conflicts=True,
                    unique_fields=['beneficiary'],
                    update_fields=['division', 'district', 'upazila', 'pouroword_or_union', 'union', 'ward_no', 'village', 'village_other', 'household_identification', 'latitude', 'longitude']
                )

                BeneficiaryAttachment.objects.bulk_create(
                    attachment_objs,
                    update_conflicts=True,
                    unique_fields=['beneficiary'],
                    update_fields=['attachment_photo', 'attachment_nid_doc', 'attachment_brn_doc', 'attachment_hh_head_nid_doc', 'attachment_testimonial_or_certificate', 'education_certificate', 'testimonial', 'training_certificate']
                )

                BeneficiaryHouseHoldInfo.objects.bulk_create(
                    household_objs,
                    update_conflicts=True,
                    unique_fields=['beneficiary'],
                    update_fields=['hh_head_name_en', 'hh_head_name_bn', 'hh_head_gender', 'hh_head_nid', 'hh_total_members', 'hh_count_1535', 'hh_count_1535_collected', 'hh_count_1535_uncollected_reason', 'hh_count_earning', 'is_indigenous', 'indigenous_group_type', 'indigenous_group_others', 'household_special_area', 'household_special_area_specify']
                )

                BeneficiaryDifficulty.objects.bulk_create(
                    difficulty_objs,
                    update_conflicts=True,
                    unique_fields=['beneficiary'],
                    update_fields=['seeing', 'hearing', 'walking', 'remembering', 'selfcare', 'communicating', 'is_pwd']
                )

                BeneficiaryEducationInfo.objects.bulk_create(
                    education_objs,
                    update_conflicts=True,
                    unique_fields=['beneficiary'],
                    update_fields=['currently_in_education', 'highest_education_level', 'other_education_level', 'institution_type', 'madrasha_type', 'attended_classes_last_6_months', 'ever_dropped_out', 'discontinue_reason', 'discontinue_reason_others', 'attended_govt_job_exam_last_6_months', 'can_read_bangla', 'can_write_bangla', 'can_read_english', 'can_write_english']
                )

                BeneficiaryEmploymentInfo.objects.bulk_create(
                    employment_objs,
                    update_conflicts=True,
                    unique_fields=['beneficiary'],
                    update_fields=['is_currently_employed', 'employment_status_self_or_wage', 'current_employment_type', 'wage_employment_status', 'employment_status_others', 'income_last_month', 'avg_income_6months', 'unemployment_months', 'has_work_experience', 'experience_years', 'left_work_reason', 'left_work_reason_others', 'currently_in_training', 'received_skill_training_go_ngo', 'has_vocational_certificate', 'training_project_name', 'training_project_name_others', 'training_months_ago', 'training_trade', 'is_potential_beneficiary']
                )

                BeneficiaryDigitalSkill.objects.bulk_create(
                    digital_skill_objs,
                    update_conflicts=True,
                    unique_fields=['beneficiary'],
                    update_fields=['has_smartphone', 'has_computer_or_laptop', 'computer_skill', 'uses_internet', 'app_usage', 'knows_driving', 'vehicle_type', 'has_driving_licence', 'received_driving_training', 'driving_training_location', 'driving_training_location_others']
                )

                BeneficiaryWillingnessInfo.objects.bulk_create(
                    willingness_objs,
                    update_conflicts=True,
                    unique_fields=['beneficiary'],
                    update_fields=['livelihood_plan', 'searching_employment', 'has_employment_challenges', 'employment_challenge_type', 'employment_challenge_others', 'interested_in_training', 'has_onsite_training_challenges', 'onsite_training_challenge_types', 'onsite_training_challenge_others', 'comfortable_online_training']
                )

                total_success += len(beneficiary_objs)

                if self.celery_task:
                    self.celery_task.update_state(
                        state='PROGRESS',
                        meta={'processed': total_success, 'total': total_rows}
                    )

        return {'status': 'Completed', 'total_processed': total_success}

    @staticmethod
    def _clean_str(val):
        if pd.isna(val) or val is None:
            return None
        val_str = str(val).strip()
        return val_str[:-2] if val_str.endswith('.0') else val_str

    @staticmethod
    def _clean_nid_or_brn(val):
        if pd.isna(val) or not val:
            return None
        val_str = str(val).strip()
        if val_str.endswith('.0'):
            val_str = val_str[:-2]
        if '*' in val_str or '?' in val_str:
            return None
        digits_only = re.sub(r'\D', '', val_str)
        return digits_only if digits_only else None

    @staticmethod
    def _clean_phone(val):
        if pd.isna(val) or not val:
            return None
        val_str = str(val).strip()
        if val_str.endswith('.0'):
            val_str = val_str[:-2]
        if '*' in val_str or '?' in val_str:
            return None
        digits_only = re.sub(r'\D', '', val_str)
        return digits_only if digits_only else None
    
    @staticmethod
    def _parse_relation_to_hh_head(val):
        if pd.isna(val) or val is None:
            return None
        val_str = str(val).strip()
        if val_str.endswith('.0'):
            val_str = val_str[:-2]
        try:
            val_int = int(val_str)
            if val_int in _VALID_RELATION_CODES:   
                return val_int
        except ValueError:
            pass
        return None

    @staticmethod
    def _parse_date(date_str):
        if pd.isna(date_str) or not date_str:
            return None
        date_str = str(date_str).strip()
        if '*' in date_str or '?' in date_str:
            years = re.findall(r'\b\d{4}\b', date_str)
            if years:
                return date(int(years[0]), 1, 1)
            return None
        if 'T' in date_str:
            date_str = date_str.split('T')[0]
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return None

    @staticmethod
    def _parse_bool(val):
        if pd.isna(val) or val is None:
            return False
        val_str = str(val).strip().lower()
        if val_str.endswith('.0'):
            val_str = val_str[:-2]
        return val_str in ['1', 'true', 'yes', 'হ্যাঁ']

    @staticmethod
    def _calculate_age(dob, ref_date):
        if not dob:
            return None
        today = ref_date if ref_date else date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    # @staticmethod
    # def _parse_int(val):
    #     if pd.isna(val) or val is None:
    #         return 0
    #     val_str = str(val).strip()
    #     if val_str.endswith('.0'):
    #         val_str = val_str[:-2]
    #     return int(val_str) if val_str.isdigit() else 0

    @staticmethod
    def _parse_int(val, choices_or_cls=None):
        if pd.isna(val) or val is None:
            return 0
        val_str = str(val).strip()
        if val_str.endswith('.0'):
            val_str = val_str[:-2]
            
        if not val_str.isdigit():
            return 0

        val_int = int(val_str)

        # যদি choices পাঠানো হয়ে থাকে তবে ভ্যালিডেশন চেক করবে
        if choices_or_cls:
            if hasattr(choices_or_cls, 'choices'):
                valid_values = {int(choice[0]) for choice in choices_or_cls.choices}
            else:
                valid_values = {int(choice[0]) for choice in choices_or_cls}

            return val_int if val_int in valid_values else 0

        return val_int


    @staticmethod
    def _parse_multi_choice(val):
        if pd.isna(val) or not val:
            return None
        
        val_str = str(val).strip()
        if val_str.endswith('.0'):
            val_str = val_str[:-2]
            
        # কমা (,), পাইপ (|) বা স্পেস দিয়ে স্প্লিট করে শুধু ডিজিটগুলোকে ফিল্টার করা
        extracted_digits = re.findall(r'\d+', val_str)
        
        # Valid choices filter (1, 2, 3)
        valid_choices = {choice.value for choice in HHCountUncollectedReasonChoices}
        selected = [d for d in extracted_digits if d in valid_choices]
        
        # ডুপ্লিকেট রিমুভ করে কমা দিয়ে জয়েন করা ("1,2")
        return ",".join(sorted(list(set(selected)))) if selected else None

    @staticmethod
    def _parse_disability_choice(val, choices_or_cls):
        if pd.isna(val) or val is None:
            return None

        val_str = str(val).strip()
        if val_str.endswith('.0'):
            val_str = val_str[:-2]

        try:
            val_int = int(val_str)
            
            # যদি choices_or_cls একটি Django TextChoices/IntegerChoices ক্লাস হয়
            if hasattr(choices_or_cls, 'choices'):
                valid_values = {int(choice[0]) for choice in choices_or_cls.choices}
            # যদি এটি সরাসরি [(180, 'Label'), ...] টাইপের লিস্ট/টুপল হয়
            else:
                valid_values = {int(choice[0]) for choice in choices_or_cls}

            if val_int in valid_values:
                return val_int
        except (ValueError, TypeError):
            pass

        return None
    
    @staticmethod
    def _parse_multi_choice_text(val):
        """
        এক্সেল/CSV ডাটা থেকে সব ডিজিট এক্সট্র্যাক্ট করে কমা-সেপারেটেড স্ট্রিং (যেমন: '1,2,3') তৈরি করে।
        """
        if pd.isna(val) or not val:
            return None
            
        val_str = str(val).strip()
        if val_str.endswith('.0'):
            val_str = val_str[:-2]
            
        # সব সংখ্যা ডিজিট হিসেবে এক্সট্র্যাক্ট করা (যেমন: "1,2,3" -> ['1', '2', '3'])
        extracted_digits = re.findall(r'\d+', val_str)
        
        if not extracted_digits:
            return None
            
        # ডুপ্লিকেট বাদ দিয়ে সাজিয়ে কমা দিয়ে যুক্ত করা (যেমন: "1,2,3")
        unique_sorted_digits = sorted(list(set(extracted_digits)))
        return ",".join(unique_sorted_digits)
    
    @staticmethod
    def _parse_float(val):
        if pd.isna(val) or val is None:
            return None
        
        val_str = str(val).strip()
        
        # ১. ইংরেজি/বাংলা ডিজিট ম্যাপ
        bangla_to_eng = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
        val_str = val_str.translate(bangla_to_eng)
        
        # ২. কমা (,) বা স্পেস মুছে ফেলা (যেমন: 12,500.00 -> 12500.00)
        val_str = val_str.replace(',', '').replace(' ', '')
        
        # ৩. ফ্লোট-এ কনভার্ট করার চেষ্টা করা
        try:
            return float(val_str)
        except (ValueError, TypeError):
            return None