from django.db import models
from django.contrib.auth.models import User
from apps.core.models import Location

# 1. Admin Master Template
class EarnTaskTemplate(models.Model):
    class Segment(models.TextChoices):
        INCEPTION = 'Inception', 'Inception'
        CG_FORMATION = 'CG Formation', 'CG Formation'
        VLTC_SITE = 'VLTC Site', 'VLTC Site'
        BENEFICIARY = 'Beneficiary', 'Beneficiary'
        EMPLOYABILITY = 'Employability', 'Employability'

    class RoleChoice(models.TextChoices):
        LEAD = 'Lead', 'Lead'
        SUPPORT = 'Support', 'Support'
        KEY_SUPPORT = 'Key Support', 'Key Support'

    segment = models.CharField(max_length=50, choices=Segment.choices)
    task_name = models.CharField(max_length=255)
    um_role = models.CharField(max_length=20, choices=RoleChoice.choices, default=RoleChoice.SUPPORT)
    jpo_role = models.CharField(max_length=20, choices=RoleChoice.choices, default=RoleChoice.SUPPORT)
    edo_role = models.CharField(max_length=20, choices=RoleChoice.choices, default=RoleChoice.SUPPORT)
    output = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    guideline_doc = models.FileField(upload_to='earn_task_guidelines/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'earn_task_template'

    def __str__(self):
        return f"{self.task_name} ({self.segment})"


# 2. Upazila User Submission
class EarnTaskSubmission(models.Model):
    class StatusChoice(models.TextChoices):
        DONE = 'Done', 'Done'
        DUE_SOON = 'Due Soon', 'Due Soon'
        UPCOMING = 'Upcoming', 'Upcoming'
        ONGOING = 'Ongoing', 'Ongoing'
        NOT_SET = 'Not Set', 'Not Set'

    task_template = models.ForeignKey(EarnTaskTemplate, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Location Hierarchy
    division = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='task_sub_division')
    district = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='task_sub_district')
    upazila = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='task_sub_upazila')

    # Upazila Inputs
    status = models.CharField(max_length=20, choices=StatusChoice.choices, default=StatusChoice.NOT_SET)
    attachment = models.FileField(upload_to='earn_task_submissions/', blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'earn_task_submission'
        unique_together = ('task_template', 'upazila')

    def __str__(self):
        return f"{self.upazila.name_en} - {self.task_template.task_name} ({self.status})"