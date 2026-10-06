from django.db import models
from apps.programs.models import Program


class Project(models.Model):
    PROJECT_STATUS = (
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
    )

    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name='projects',
        help_text="প্রজেক্টটি যে প্রোগ্রাম-এর অধীনে থাকবে"
    )

    code = models.CharField(max_length=150, unique=True, help_text="e.g. EARN, NSC, AGROECOLOGY")
    title = models.CharField(max_length=255)
    donor = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.TextField(blank=True, null=True)
    location =  models.TextField(blank=True, null=True)
    target_beneficiaries = models.PositiveIntegerField(
        default=0, 
        help_text="প্রজেক্টের লক্ষ্যমাত্রিক মোট বেনিফিশিয়ারি সংখ্যা"
    )
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.title}"