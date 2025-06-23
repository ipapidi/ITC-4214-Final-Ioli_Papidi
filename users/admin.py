from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import UserProfile, Wishlist, RecentlyViewed, UserPreference


class UserProfileInline(admin.StackedInline):
    """
    Inline admin for user profiles.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fieldsets = (
        ('Personal Information', {
            'fields': ('phone_number', 'date_of_birth', 'profile_picture')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Car Information', {
            'fields': ('primary_car_make', 'primary_car_model', 'primary_car_year', 'car_color')
        }),
        ('F1 Preferences', {
            'fields': ('performance_style', 'favorite_f1_team', 'favorite_driver')
        }),
        ('Notifications', {
            'fields': ('email_notifications', 'sms_notifications', 'newsletter_subscription')
        }),
        ('Account', {
            'fields': ('is_verified', 'verification_token', 'last_login_ip')
        }),
    )


class UserPreferenceInline(admin.StackedInline):
    """
    Inline admin for user preferences.
    """
    model = UserPreference
    can_delete = False
    verbose_name_plural = 'Preferences'
    fieldsets = (
        ('Display', {
            'fields': ('theme',)
        }),
        ('Product Preferences', {
            'fields': ('preferred_categories', 'preferred_brands', 'price_range_min', 'price_range_max')
        }),
        ('Notifications', {
            'fields': ('email_frequency',)
        }),
        ('Privacy', {
            'fields': ('profile_visibility',)
        }),
    )


class UserAdmin(BaseUserAdmin):
    """
    Extended user admin with profile and preferences.
    """
    inlines = [UserProfileInline, UserPreferenceInline]
    list_display = ['username', 'email', 'full_name', 'car_info', 'is_verified', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined', 'profile__is_verified']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'profile__primary_car_make']
    readonly_fields = ['date_joined', 'last_login']

    def full_name(self, obj):
        """Display user's full name"""
        return obj.profile.get_full_name()
    full_name.short_description = 'Full Name'

    def car_info(self, obj):
        """Display user's car information"""
        return obj.profile.get_car_info()
    car_info.short_description = 'Car'

    def is_verified(self, obj):
        """Display verification status"""
        if obj.profile.is_verified:
            return format_html('<span style="color: #27ae60;">✓ Verified</span>')
        return format_html('<span style="color: #e74c3c;">✗ Not Verified</span>')
    is_verified.short_description = 'Verified'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """
    Admin interface for user wishlists.
    """
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['added_at']
    ordering = ['-added_at']


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    """
    Admin interface for recently viewed products.
    """
    list_display = ['user', 'product', 'view_count', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['viewed_at']
    ordering = ['-viewed_at']
