from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
import os
import re


def validate_file_size(value):
    #Validate file size (max 5MB)
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("File size cannot exceed 5MB")

def validate_file_type(value):
    #Validate file type (images only)
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only image files are allowed.')

def validate_phone_number(value):
    """Validate phone number format"""
    if not value:
        return value
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', value)
    
    if len(digits_only) < 10:
        raise ValidationError('Phone number must have at least 10 digits.')
    
    if len(digits_only) > 15:
        raise ValidationError('Phone number cannot exceed 15 digits.')
    
    return value

def validate_postal_code(value):
    """Validate postal code format"""
    if not value:
        return value
    
    # Allow alphanumeric characters, spaces, and hyphens
    if not re.match(r'^[A-Za-z0-9\s\-]+$', value):
        raise ValidationError('Postal code can only contain letters, numbers, spaces, and hyphens.')
    
    if len(value.strip()) < 3:
        raise ValidationError('Postal code must be at least 3 characters long.')
    
    if len(value.strip()) > 10:
        raise ValidationError('Postal code cannot exceed 10 characters.')
    
    return value.strip()

def validate_address(value):
    """Validate address fields"""
    if not value:
        return value
    
    if len(value.strip()) < 5:
        raise ValidationError('Address must be at least 5 characters long.')
    
    if len(value.strip()) > 255:
        raise ValidationError('Address cannot exceed 255 characters.')
    
    # Check for potentially harmful content
    harmful_patterns = [
        r'<script|javascript:|vbscript:|onload=|onerror=',
        r'\b(www\.|http://|https://)\b',
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError('Address contains invalid content.')
    
    return value.strip()


class UserProfile(models.Model):
    # User profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[validate_phone_number],
        help_text="Phone number (10-15 digits)"
    )
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, validators=[validate_file_size, validate_file_type])
    
    # Address Information
    address_line1 = models.CharField(
        max_length=255, 
        blank=True, 
        validators=[validate_address],
        help_text="Address line 1 (5-255 characters)"
    )
    address_line2 = models.CharField(
        max_length=255, 
        blank=True, 
        validators=[validate_address],
        help_text="Address line 2 (5-255 characters)"
    )
    city = models.CharField(
        max_length=100, 
        blank=True,
        help_text="City name (max 100 characters)"
    )
    state = models.CharField(
        max_length=100, 
        blank=True,
        help_text="State/province (max 100 characters)"
    )
    postal_code = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[validate_postal_code],
        help_text="Postal code (3-10 characters)"
    )
    country = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Country name (max 100 characters)"
    )
    
    # Vendor Information
    is_vendor = models.BooleanField(default=False, help_text="Is this user a vendor?")
    vendor_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Approval'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending',
        help_text="Vendor approval status"
    )
    vendor_team = models.CharField(max_length=100, blank=True, help_text="F1 team this vendor represents")
    vendor_application_date = models.DateTimeField(blank=True, null=True)
    vendor_approved_date = models.DateTimeField(blank=True, null=True)
    vendor_approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='approved_vendors',
        help_text="Admin who approved this vendor"
    )
    
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

    def is_verified_vendor(self):
        # Check if user is a verified vendor
        return self.is_vendor and self.vendor_status == 'approved'

    def get_vendor_badge(self):
        # Get vendor badge text
        if self.is_verified_vendor():
            return "Verified Vendor"
        elif self.is_vendor and self.vendor_status == 'pending':
            return "Vendor (Pending)"
        elif self.is_vendor and self.vendor_status == 'rejected':
            return "Vendor (Rejected)"
        return None


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
        # make user profile
        UserProfile.objects.create(user=instance)
        UserPreference.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # save profile and prefs
    instance.profile.save()
    instance.preferences.save()
