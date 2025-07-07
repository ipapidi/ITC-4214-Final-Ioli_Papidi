from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os


def validate_file_size(value):
    """Validate file size (max 5MB)"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("File size cannot exceed 5MB")

def validate_file_type(value):
    """Validate file type (images only)"""
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only image files are allowed.')


class UserProfile(models.Model):
    # User profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, validators=[validate_file_size, validate_file_type])
    
    # Address Information
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Car Information
    primary_car_make = models.CharField(max_length=100, blank=True, help_text="e.g., Ferrari, Mercedes, BMW")
    primary_car_model = models.CharField(max_length=100, blank=True, help_text="e.g., F8 Tributo, AMG GT, M3")
    primary_car_year = models.PositiveIntegerField(blank=True, null=True)
    car_color = models.CharField(max_length=50, blank=True)
    
    # Performance Preferences
    performance_style = models.CharField(
        max_length=20,
        choices=[
            ('track', 'Track Performance'),
            ('street', 'Street Performance'),
            ('show', 'Show Car'),
            ('daily', 'Daily Driver'),
            ('f1_inspired', 'F1 Inspired')
        ],
        default='street'
    )
    
    # F1 Team Preferences
    favorite_f1_team = models.CharField(max_length=100, blank=True)
    favorite_driver = models.CharField(max_length=100, blank=True)
    
    # Notification Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    newsletter_subscription = models.BooleanField(default=True)
    
    # Account Settings
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Profile for {self.user.username}"

    def get_full_name(self):
        # Get user's full name
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

    def get_car_info(self):
        # Get formatted car information
        if self.primary_car_make and self.primary_car_model:
            year = f" {self.primary_car_year}" if self.primary_car_year else ""
            return f"{self.primary_car_make} {self.primary_car_model}{year}"
        return "No car specified"


class Wishlist(models.Model):
    # User wishlist
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Personal notes about this product")

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class RecentlyViewed(models.Model):
    # Recently viewed products
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='viewed_by')
    viewed_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.user.username} viewed {self.product.name}"


class UserPreference(models.Model):
    # User preferences
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Display Preferences
    theme = models.CharField(
        max_length=20,
        choices=[
            ('dark', 'Dark Theme'),
            ('light', 'Light Theme'),
            ('auto', 'Auto (System)')
        ],
        default='dark'
    )
    
    # Product Preferences
    preferred_categories = models.ManyToManyField('products.Category', blank=True)
    preferred_brands = models.ManyToManyField('products.Brand', blank=True)
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_range_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Notification Settings
    email_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('never', 'Never')
        ],
        default='weekly'
    )
    
    # Privacy Settings
    profile_visibility = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('friends', 'Friends Only'),
            ('private', 'Private')
        ],
        default='public'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"


# Signal to create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserPreference.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.preferences.save()
