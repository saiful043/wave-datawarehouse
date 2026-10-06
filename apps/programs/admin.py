from django.contrib import admin
from .models import Program

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    # এডমিন লিস্ট পেজে যেসব কলাম দেখা যাবে
    list_display = ('id', 'name', 'code', 'created_at', 'updated_at')
    
    # যেসব ফিল্ড দিয়ে সার্চ করা যাবে
    search_fields = ('name', 'code')
    
    # যেসব ফিল্ডে ক্লিক করে বিস্তারিত দেখা/এডিট করা যাবে
    list_display_links = ('id', 'name', 'code')
    
    # ডানপাশে ফিল্টার অপশন
    list_filter = ('created_at',)
    
    # শুধুমাত্র পড়ার জন্য (Edit করা যাবে না)
    readonly_fields = ('created_at', 'updated_at')
    
    # পেজিনেশন (প্রতি পেজে ২০টি করে ডাটা দেখাবে)
    list_per_page = 20