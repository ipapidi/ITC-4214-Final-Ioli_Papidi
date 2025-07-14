from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import UserProfile, Wishlist, RecentlyViewed, UserPreference


class UserProfileInline(admin.StackedInline):
    """
    Inline admin for user profiles.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'  # Specify which ForeignKey to use
    fieldsets = (
        ('Personal Information', {
            'fields': ('phone_number', 'date_of_birth', 'profile_picture')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Vendor Information', {
            'fields': ('is_vendor', 'vendor_status', 'vendor_team', 'vendor_application_date', 'vendor_approved_date', 'vendor_approved_by'),
            'classes': ('collapse',)
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
    fk_name = 'user'
    fieldsets = (
        ('Display Preferences', {
            'fields': ('theme',)
        }),
        ('Product Preferences', {
            'fields': ('preferred_categories', 'preferred_brands', 'price_range_min', 'price_range_max')
        }),
        ('Privacy Settings', {
            'fields': ('profile_visibility',)
        }),
    )


class UserAdmin(BaseUserAdmin):
    """
    Extended user admin with profile and preferences.
    """
    inlines = [UserProfileInline, UserPreferenceInline]
    list_display = ['username', 'email', 'full_name', 'vendor_status', 'is_verified', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined', 'profile__is_verified', 'profile__is_vendor', 'profile__vendor_status']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'profile__vendor_team']
    readonly_fields = ['date_joined', 'last_login']
    actions = ['approve_vendors', 'reject_vendors']

    def full_name(self, obj):
        """Display user's full name"""
        return obj.profile.get_full_name()
    full_name.short_description = 'Full Name'

    def vendor_status(self, obj):
        """Display vendor status"""
        if obj.profile.is_vendor:
            status = obj.profile.vendor_status
            if status == 'approved':
                return format_html('<span style="color: #27ae60;">✓ Approved Vendor</span>')
            elif status == 'pending':
                return format_html('<span style="color: #f39c12;">Pending</span>')
            elif status == 'rejected':
                return format_html('<span style="color: #e74c3c;">✗ Rejected</span>')
        return format_html('<span style="color: #95a5a6;">Not a Vendor</span>')
    vendor_status.short_description = 'Vendor Status'

    def is_verified(self, obj):
        """Display verification status"""
        if obj.profile.is_verified:
            return format_html('<span style="color: #27ae60;">✓ Verified</span>')
        return format_html('<span style="color: #e74c3c;">✗ Not Verified</span>')
    is_verified.short_description = 'Verified'

    def approve_vendors(self, request, queryset):
        """Admin action to approve vendors"""
        updated = 0
        for user in queryset:
            if user.profile.is_vendor and user.profile.vendor_status == 'pending':
                user.profile.vendor_status = 'approved'
                user.profile.vendor_approved_date = timezone.now()
                user.profile.vendor_approved_by = request.user
                user.profile.save()
                updated += 1
        
        if updated == 1:
            self.message_user(request, f'{updated} vendor application approved.')
        else:
            self.message_user(request, f'{updated} vendor applications approved.')
    approve_vendors.short_description = "Approve selected vendor applications"

    def reject_vendors(self, request, queryset):
        """Admin action to reject vendors"""
        updated = 0
        for user in queryset:
            if user.profile.is_vendor and user.profile.vendor_status == 'pending':
                user.profile.vendor_status = 'rejected'
                user.profile.save()
                updated += 1
        
        if updated == 1:
            self.message_user(request, f'{updated} vendor application rejected.')
        else:
            self.message_user(request, f'{updated} vendor applications rejected.')
    reject_vendors.short_description = "Reject selected vendor applications"


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
