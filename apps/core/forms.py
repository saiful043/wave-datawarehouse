from django import forms
from django_select2.forms import ModelSelect2Widget, Select2Widget
from apps.core.models import Location


class LocationAdminFilterForm(forms.Form):
    # বিভাগ: পেজ লোড হলেই ৮টি বিভাগ সরাসরি লোড হবে
    division = forms.ModelChoiceField(
        queryset=Location.objects.filter(type=2, parent_location_id=1),
        required=False,
        label="বিভাগ",
        empty_label="--- বিভাগ নির্বাচন করুন ---",
        # widget=Select2Widget(
        #    attrs={
                  
        #         'class': 'custom-select2'
        #     }
        # )
    )

    # জেলা: বিভাগের ওপর নির্ভর করে টাইপ বা সার্চে লোড হবে
    district = forms.ModelChoiceField(
        queryset=Location.objects.filter(type=3),
        required=False,
        label="জেলা",
        widget=ModelSelect2Widget(
            model=Location,
            search_fields=['name_bn__icontains', 'name_en__icontains'],
            dependent_fields={'division': 'parent_location_id'},
        #    attrs={
        #         'data-width': '100%',  # 👈 Select2-কে পুরো প্যারেন্ট ডিবের সাইজ নিতে বাধ্য করবে
        #         'class': 'custom-select2'
        #     }
        )
    )

    # উপজেলা: জেলার ওপর নির্ভর করে লোড হবে
    upazila = forms.ModelChoiceField(
        queryset=Location.objects.filter(type=4),
        required=False,
        label="উপজেলা",
        widget=ModelSelect2Widget(
            model=Location,
            search_fields=['name_bn__icontains', 'name_en__icontains'],
            dependent_fields={'district': 'parent_location_id'},
        #    attrs={
        #         'data-width': '100%',  # 👈 Select2-কে পুরো প্যারেন্ট ডিবের সাইজ নিতে বাধ্য করবে
        #         'class': 'custom-select2'
        #     }
        )
    )