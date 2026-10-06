from django.db import models

class Location(models.Model):
    location_id = models.IntegerField(primary_key=True) # API-এর "id"
    name_en = models.CharField(max_length=255, null=True, blank=True)
    name_bn = models.CharField(max_length=255, null=True, blank=True)
    parent_location_id = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    path_string = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    bbs_code = models.CharField(max_length=50, null=True, blank=True)
    bbs_code_path = models.CharField(max_length=255, null=True, blank=True)
    bbs_version_id = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['parent_location_id', 'type']), # Composite index
        ]

    def __str__(self):
        return f"{self.name_en or self.name_bn} ({self.location_id})"


class Gender(models.Model):
    label_en = models.CharField(max_length=50)
    label_bn = models.CharField(max_length=50)
    status = models.IntegerField(default=1)  # 1 = Active, 0 = Inactive
    score = models.IntegerField(default=0)
    color_hex = models.CharField(max_length=7, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    visible_when = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Gender'
        verbose_name_plural = 'Genders'
        indexes = [
            # status এবং display_order দিয়ে ফিল্টার ও সর্টিং ফাস্ট করার জন্য Composite Index
            models.Index(fields=['status', 'display_order']),
        ]

    def __str__(self):
        return f"{self.label_en} ({self.label_bn})"

class IndigenousGroupType(models.Model):
    label_en = models.CharField(max_length=100)
    label_bn = models.CharField(max_length=100)
    status = models.IntegerField(default=1)  # 1 = Active, 0 = Inactive
    score = models.IntegerField(default=0)
    color_hex = models.CharField(max_length=7, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    visible_when = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'core_indigenous_group_type'
        ordering = ['display_order', 'id']
        verbose_name = 'Indigenous Group Type'
        verbose_name_plural = 'Indigenous Group Types'
        indexes = [
            # status এবং display_order দিয়ে ফিল্টার ও সর্টিং ফাস্ট করার জন্য Composite Index
            models.Index(fields=['status', 'display_order']),
        ]

    def __str__(self):
        return f"{self.label_en} ({self.label_bn})"

class Package(models.Model):
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name_en = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    survey_target = models.PositiveIntegerField(default=0)
    total_beneficiary_target = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_package'
        ordering = ['sort_order', 'id']
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'
        indexes = [
            models.Index(fields=['sort_order', 'code']),
        ]

    def __str__(self):
        return f"{self.name_en} ({self.code})"