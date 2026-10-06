from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.core.models import Location, Gender, IndigenousGroupType, Package



@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    # লিস্ট ভিউতে যে কলামগুলো দেখাবে
    list_display = (
        'location_id', 
        'name_en', 
        'name_bn', 
        'type', 
        'code', 
        'parent_location_id'
    )
    
    # ডানপাশে ফিল্টার করার অপশন
    list_filter = ('type',)
    
    # সার্চ বার (ইংরেজি ও বাংলা নাম এবং আইডি দিয়ে খোঁজা যাবে)
    search_fields = (
        'location_id', 
        'name_en', 
        'name_bn', 
        'code', 
        'bbs_code'
    )
    
    # প্রতি পেজে কতটি করে ডাটা দেখাবে
    list_per_page = 50
    
    # শুধু পড়ার জন্য (অ্যাক্সিডেন্টালি এডিট হওয়া ঠেকাতে চাইলে রাখতে পারেন)
    readonly_fields = ('location_id', 'path_string', 'bbs_code_path')
    
    # ডাটা সাজানোর ক্রম
    ordering = ('location_id',)

@admin.register(Gender)
class GenderAdmin(ModelAdmin):
    list_display = (
        'id',
        'label_en',
        'label_bn',
        'status',
        'score',
        'color_hex',
        'display_order',
    )
    list_editable = ('status', 'score', 'display_order')
    search_fields = ('label_en', 'label_bn')
    list_filter = ('status',)
    ordering = ('display_order', 'id')

@admin.register(IndigenousGroupType)
class IndigenousGroupTypeAdmin(ModelAdmin):
    list_display = (
        'id',
        'label_en',
        'label_bn',
        'status',
        'score',
        'color_hex',
        'display_order',
    )
    list_editable = ('status', 'score', 'display_order')
    search_fields = ('label_en', 'label_bn')
    list_filter = ('status',)
    ordering = ('display_order', 'id')

@admin.register(Package)
class PackageAdmin(ModelAdmin):
    list_display = (
        'id',
        'code',
        'name_en',
        'name_bn',
        'sort_order',
        'survey_target',
        'total_beneficiary_target',
        'updated_at'
    )
    list_editable = ('sort_order', 'survey_target', 'total_beneficiary_target')
    search_fields = ('code', 'name_en', 'name_bn')
    ordering = ('sort_order', 'id')
    list_per_page = 20