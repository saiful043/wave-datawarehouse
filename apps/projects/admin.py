from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Project


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ('code', 'title', 'donor', 'status', 'duration')
    search_fields = ('code', 'title', 'donor')
    list_filter = ('status',)
# Register your models here.
