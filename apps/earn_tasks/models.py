from django.db import models
from django.contrib.auth.models import User
from apps.core.models import Location


class EarnParentTask(models.Model):
    task_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'earn_parent_task'
        verbose_name = 'Earn Parent Task'
        verbose_name_plural = 'Earn Parent Tasks'

    def __str__(self):
        return f"{self.name} ({self.task_id})"

# 1. Admin Master Template
class EarnTaskTemplate(models.Model):
    class LevelChoice(models.TextChoices):
        HQ = 'HQ', 'HQ'
        UPAZILA = 'Upazila', 'Upazila'

    parent_task = models.ForeignKey(
        EarnParentTask,
        on_delete=models.CASCADE,
        related_name='task_templates',
        db_column='earn_parent_task_id',
        null=True,
        blank=True
    )
    task_code = models.CharField(max_length=100, blank=True, null=True)
    task_name = models.CharField(max_length=400)
    
    planned_period_from = models.DateField(blank=True, null=True)
    planned_period_to = models.DateField(blank=True, null=True)
    
    # Level as CharField with Choices
    level = models.CharField(
        max_length=50, 
        choices=LevelChoice.choices, 
        default=LevelChoice.HQ
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'earn_task_template'

    def __str__(self):
        return f"{self.task_name} (Level: {self.level})"


# 2. Upazila User Submission
class EarnTaskSubmission(models.Model):
    class StatusChoice(models.TextChoices):
        NOT_STARTED = 'Not Started', 'Not Started'
        IN_PROGRESS = 'In Progress', 'In Progress'
        COMPLETED = 'Completed', 'Completed'
        DELAYED = 'Delayed', 'Delayed'

    task_template = models.ForeignKey(EarnTaskTemplate, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Location Hierarchy
    division = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='task_sub_division')
    district = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='task_sub_district')
    upazila = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='task_sub_upazila')

    # Upazila Inputs
    status = models.CharField(max_length=20, choices=StatusChoice.choices, default=StatusChoice.NOT_STARTED)
    # attachment = models.FileField(upload_to='earn_task_submissions/', blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    percentage_completion = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    submitted_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'earn_task_submission'
        unique_together = ('task_template', 'upazila')

    def __str__(self):
        return f"{self.upazila.name_en} - {self.task_template.task_name} ({self.status})"