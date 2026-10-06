from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator


class FieldActivity(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    # 1. Basic Information
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 'User' এর বদলে settings.AUTH_USER_MODEL দিন
        on_delete=models.CASCADE, 
        related_name='field_activities',
        verbose_name="Manager/User"
    )
    date = models.DateField(verbose_name="Activity Date")

    # 🗺️ Geographic Location Fields (UserProfile থেকে auto-populate হবে)
    division = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='field_activities_division',
        verbose_name="Division"
    )
    district = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='field_activities_district',
        verbose_name="District"
    )
    upazila = models.ForeignKey(
        'core.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='field_activities_upazila',
        verbose_name="Upazila"
    )

    # 2. Field Visit & Purpose
    visit_area = models.CharField(
        max_length=255, 
        help_text="Union, Village, or specific area visited"
    )

    # 🌐 GPS Coordinates
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8, 
        blank=True, 
        null=True,
        help_text="e.g., 23.810332"
    )
    longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8, 
        blank=True, 
        null=True,
        help_text="e.g., 90.412518"
    )

    purpose_of_visit = models.TextField(help_text="Main objective of the visit")
    target_group = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="e.g., Farmers, Local Women Group, NGO Members"
    )
    contact_person = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Name and phone number of the key contact"
    )

    # 3. Metrics & Details
    number_of_meeting = models.PositiveIntegerField(
        default=0, 
        verbose_name="Number of Meetings"
    )
    total_person_conducted = models.PositiveIntegerField(
        default=0, 
        verbose_name="Total Attendees/People Reached"
    )
    meeting_details = models.TextField(
        blank=True, 
        null=True, 
        help_text="Summary of discussions and outcomes"
    )
    others = models.TextField(
        blank=True, 
        null=True, 
        help_text="Other notable activities or events"
    )

    # 4. Evidence & Remarks
    meeting_photo = models.ImageField(
        upload_to='field_activity_photos/%Y/%m/%d/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Upload meeting or field visit proof image"
    )
    remarks = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Admin Remarks",
        help_text="Challenges faced, issues, or manager notes"
    )

    # 5. Workflow Status & System Fields
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.SUBMITTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'field_activities'
        verbose_name = "Field Activity"
        verbose_name_plural = "Field Activities"
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['status']),
            models.Index(fields=['division', 'district', 'upazila']), # Location filtering optimization
        ]

    def save(self, *args, **kwargs):
        # 💡 Auto-populate location from UserProfile if not manually provided
        if hasattr(self.user, 'profile'):
            profile = self.user.profile
            if not self.division_id and hasattr(profile, 'division'):
                self.division = profile.division
            if not self.district_id and hasattr(profile, 'district'):
                self.district = profile.district
            if not self.upazila_id and hasattr(profile, 'upazila'):
                self.upazila = profile.upazila

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.visit_area} ({self.date})"