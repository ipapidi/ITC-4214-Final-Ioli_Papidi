from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import UserProfile, Wishlist, RecentlyViewed, UserPreference, ContactMessage


class UserProfileInline(admin.StackedInline):
    """
    Inline admin for user profiles.
    """
    model = UserProfile
    can_delete = False # Can delete
    verbose_name_plural = 'Profile' # Verbose name plural
    fk_name = 'user' # Foreign key to user
    fieldsets = ( # Fieldsets
        ('Personal Information', { # Personal information
            'fields': ('phone_number', 'date_of_birth', 'profile_picture') # Fields
        }),
        ('Address', { # Address
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country') # Fields
        }),
        ('Vendor Information', { # Vendor information
            'fields': ('is_vendor', 'vendor_status', 'vendor_team', 'vendor_application_date', 'vendor_approved_date', 'vendor_approved_by'), # Fields
            'classes': ('collapse',) # Classes
        }),
        ('Account', { # Account
            'fields': ('is_verified', 'verification_token', 'last_login_ip')
        }),
    )


class UserPreferenceInline(admin.StackedInline):
    """
    Inline admin for user preferences.
    """
    model = UserPreference # Model
    can_delete = False # Can delete
    verbose_name_plural = 'Preferences' # Verbose name plural
    fk_name = 'user' # Foreign key to user
    fieldsets = ( # Fieldsets
        ('Display Preferences', { # Display preferences
            'fields': ('theme',) # Fields
        }),
        ('Product Preferences', { # Product preferences
            'fields': ('preferred_categories', 'preferred_brands', 'price_range_min', 'price_range_max') # Fields
        }),
        ('Privacy Settings', { # Privacy settings
            'fields': ('profile_visibility',) # Fields
        }),
    )


class UserAdmin(BaseUserAdmin):
    """
    Extended user admin with profile and preferences.
    """
    inlines = [UserProfileInline, UserPreferenceInline] # Inlines
    list_display = ['username', 'email', 'full_name', 'vendor_status', 'is_verified', 'date_joined'] # List display
    list_filter = ['is_active', 'is_staff', 'date_joined', 'profile__is_verified', 'profile__is_vendor', 'profile__vendor_status'] # List filter
    search_fields = ['username', 'first_name', 'last_name', 'email', 'profile__vendor_team'] # Search fields
    readonly_fields = ['date_joined', 'last_login'] # Readonly fields
    actions = ['approve_vendors', 'reject_vendors'] # Actions

    def full_name(self, obj):
        """Display user's full name"""
        return obj.profile.get_full_name() # Return user's full name
    full_name.short_description = 'Full Name' 

    def vendor_status(self, obj):
        """Display vendor status"""
        if obj.profile.is_vendor:
            status = obj.profile.vendor_status # Vendor status
            if status == 'approved': # If vendor status is approved
                return format_html('<span style="color: #27ae60;">✓ Approved Vendor</span>') # Return approved vendor
            elif status == 'pending': # If vendor status is pending
                return format_html('<span style="color: #f39c12;">Pending</span>') # Return pending
            elif status == 'rejected': # If vendor status is rejected
                return format_html('<span style="color: #e74c3c;">✗ Rejected</span>') # Return rejected
        return format_html('<span style="color: #95a5a6;">Not a Vendor</span>') # Return not a vendor
    vendor_status.short_description = 'Vendor Status' # Short description

    def is_verified(self, obj):
        """Display verification status"""
        if obj.profile.is_verified: # If user is verified
            return format_html('<span style="color: #27ae60;">✓ Verified</span>') # Return verified
        return format_html('<span style="color: #e74c3c;">✗ Not Verified</span>') # Return not verified
    is_verified.short_description = 'Verified' # Short description

    def approve_vendors(self, request, queryset):
        """Admin action to approve vendors"""
        updated = 0 # Updated
        for user in queryset: # For each user
            if user.profile.is_vendor and user.profile.vendor_status == 'pending': # If user is vendor and vendor status is pending
                user.profile.vendor_status = 'approved' # Vendor status
                user.profile.vendor_approved_date = timezone.now() # Vendor approved date
                user.profile.vendor_approved_by = request.user # Vendor approved by
                user.profile.save() # Save user profile
                updated += 1 # Increment updated
        
        if updated == 1: # If updated is 1
            self.message_user(request, f'{updated} vendor application approved.') # Message user
        else: # If updated is not 1
            self.message_user(request, f'{updated} vendor applications approved.') # Message user
    approve_vendors.short_description = "Approve selected vendor applications" # Short description

    def reject_vendors(self, request, queryset):
        """Admin action to reject vendors"""
        updated = 0 # Updated
        for user in queryset: # For each user
            if user.profile.is_vendor and user.profile.vendor_status == 'pending': # If user is vendor and vendor status is pending
                user.profile.vendor_status = 'rejected' # Vendor status
                user.profile.save() # Save user profile
                updated += 1 # Increment updated
        
        if updated == 1: # If updated is 1
            self.message_user(request, f'{updated} vendor application rejected.') # Message user
        else: # If updated is not 1
            self.message_user(request, f'{updated} vendor applications rejected.') # Message user
    reject_vendors.short_description = "Reject selected vendor applications" # Short description


# Re-register UserAdmin
admin.site.unregister(User) # Unregister user
admin.site.register(User, UserAdmin) # Register user


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """
    Admin interface for user wishlists.
    """
    list_display = ['user', 'product', 'added_at'] # List display
    list_filter = ['added_at'] # List filter
    search_fields = ['user__username', 'product__name'] # Search fields
    readonly_fields = ['added_at'] # Readonly fields
    ordering = ['-added_at'] # Ordering


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    """
    Admin interface for recently viewed products.
    """
    list_display = ['user', 'product', 'view_count', 'viewed_at'] # List display
    list_filter = ['viewed_at'] # List filter
    search_fields = ['user__username', 'product__name'] # Search fields
    readonly_fields = ['viewed_at'] # Readonly fields
    ordering = ['-viewed_at'] # Ordering


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin): # Contact message admin
    """
    Admin interface for contact messages.
    """
    list_display = ['name', 'email', 'created_at', 'is_read', 'message_preview'] # List display
    list_filter = ['is_read', 'created_at'] # List filter
    search_fields = ['name', 'email', 'message'] # Search fields
    readonly_fields = ['created_at'] # Readonly fields
    list_editable = ['is_read'] # List editable
    
    fieldsets = ( # Fieldsets
        ('Message Details', { # Message details
            'fields': ('name', 'email', 'message') # Fields
        }),
        ('Status', { # Status
            'fields': ('is_read',) # Fields
        }),
        ('Timestamps', { # Timestamps
            'fields': ('created_at',), # Fields
            'classes': ('collapse',) # Classes
        }),
    )
    
    def message_preview(self, obj): # Message preview
        """Show first 50 characters of message"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message # Return message preview
    message_preview.short_description = 'Message Preview' # Short description
    
    actions = ['mark_as_read', 'mark_as_unread'] # Actions
    
    def mark_as_read(self, request, queryset): # Mark as read
        updated = queryset.update(is_read=True) # Update is read
        self.message_user(request, f'{updated} messages marked as read.') # Message user
    mark_as_read.short_description = "Mark selected messages as read" # Short description
    
    def mark_as_unread(self, request, queryset): # Mark as unread
        updated = queryset.update(is_read=False) # Update is read
        self.message_user(request, f'{updated} messages marked as unread.') # Message user
    mark_as_unread.short_description = "Mark selected messages as unread" # Short description
