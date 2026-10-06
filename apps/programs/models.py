from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=255, verbose_name="Program Name")
    code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Program Code")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'programs'
        verbose_name = "Program"
        verbose_name_plural = "Programs"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"