from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from apps.core.models import Location, Gender

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # লিঙ্গ / Gender (Optional)
    gender = models.ForeignKey(
        Gender, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='user_profiles'
    )

    # ভৌগোলিক স্থান / Locations (Optional)
    division = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='division_users'
    )
    district = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='district_users'
    )
    upazila = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='upazila_users'
    )
    union = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='union_users'
    )
    village = models.ForeignKey(
        Location, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='village_users'
    )

    def __str__(self):
        return f"{self.user.username}-এর প্রোফাইল"