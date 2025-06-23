from django.contrib import admin
from django.utils.html import format_html
from .models import Review, ReviewImage, ReviewVote, ProductRating, ReviewReport


class ReviewImageInline(admin.TabularInline):
    """
    Inline admin for review images.
    """
    model = ReviewImage
    extra = 0
    fields = ['image', 'caption']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for product reviews.
    Comprehensive review management with moderation features.
    """
    list_display = [
        'user', 'product', 'rating_display', 'is_verified_purchase', 
        'is_approved', 'helpful_count', 'created_at'
    ]
    list_filter = [
        'rating', 'is_verified_purchase', 'is_approved', 'is_helpful', 'created_at'
    ]
    search_fields = [
        'user__username', 'product__name', 'title', 'content'
    ]
    readonly_fields = ['created_at', 'updated_at', 'helpful_count', 'unhelpful_count']
    inlines = [ReviewImageInline]
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'product', 'rating', 'title', 'content')
        }),
        ('Additional Details', {
            'fields': ('pros', 'cons')
        }),
        ('Status', {
            'fields': ('is_verified_purchase', 'is_approved', 'is_helpful')
        }),
        ('Statistics', {
            'fields': ('helpful_count', 'unhelpful_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def rating_display(self, obj):
        """Display rating as stars"""
        return format_html(
            '<span style="color: #f39c12; font-size: 16px;">{}</span>',
            obj.rating_stars
        )
    rating_display.short_description = 'Rating'

    def helpful_count(self, obj):
        """Display helpful vote count"""
        count = obj.helpful_votes.count()
        return format_html('<span style="color: #27ae60;">{}</span>', count)
    helpful_count.short_description = 'Helpful'

    def unhelpful_count(self, obj):
        """Display unhelpful vote count"""
        count = obj.unhelpful_votes.count()
        return format_html('<span style="color: #e74c3c;">{}</span>', count)
    unhelpful_count.short_description = 'Unhelpful'

    actions = ['approve_reviews', 'disapprove_reviews', 'mark_helpful', 'mark_unhelpful']

    def approve_reviews(self, request, queryset):
        """Approve selected reviews"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} reviews approved.')
    approve_reviews.short_description = "Approve selected reviews"

    def disapprove_reviews(self, request, queryset):
        """Disapprove selected reviews"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} reviews disapproved.')
    disapprove_reviews.short_description = "Disapprove selected reviews"

    def mark_helpful(self, request, queryset):
        """Mark selected reviews as helpful"""
        updated = queryset.update(is_helpful=True)
        self.message_user(request, f'{updated} reviews marked as helpful.')
    mark_helpful.short_description = "Mark selected reviews as helpful"

    def mark_unhelpful(self, request, queryset):
        """Mark selected reviews as unhelpful"""
        updated = queryset.update(is_helpful=False)
        self.message_user(request, f'{updated} reviews marked as unhelpful.')
    mark_unhelpful.short_description = "Mark selected reviews as unhelpful"


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    """
    Admin interface for review images.
    """
    list_display = ['review', 'image_display', 'caption', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['review__user__username', 'review__product__name', 'caption']
    readonly_fields = ['uploaded_at']

    def image_display(self, obj):
        """Display review image"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 80px;" />',
                obj.image.url
            )
        return "No Image"
    image_display.short_description = 'Image'


@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    """
    Admin interface for review votes.
    """
    list_display = ['review', 'user', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['review__user__username', 'user__username', 'review__product__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    """
    Admin interface for product rating summaries.
    """
    list_display = [
        'product', 'average_rating_display', 'total_reviews', 
        'rating_percentage', 'last_updated'
    ]
    list_filter = ['last_updated']
    search_fields = ['product__name', 'product__brand__name']
    readonly_fields = [
        'average_rating', 'total_reviews', 'five_star_count', 'four_star_count',
        'three_star_count', 'two_star_count', 'one_star_count', 'last_updated'
    ]

    def average_rating_display(self, obj):
        """Display average rating as stars"""
        return format_html(
            '<span style="color: #f39c12; font-size: 16px;">{}</span>',
            obj.rating_stars
        )
    average_rating_display.short_description = 'Average Rating'

    def rating_percentage(self, obj):
        """Display percentage of positive reviews"""
        return format_html(
            '<span style="color: #27ae60; font-weight: bold;">{}%</span>',
            obj.rating_percentage
        )
    rating_percentage.short_description = 'Positive %'

    actions = ['update_ratings']

    def update_ratings(self, request, queryset):
        """Update ratings for selected products"""
        updated = 0
        for rating in queryset:
            rating.update_ratings()
            updated += 1
        self.message_user(request, f'Ratings updated for {updated} products.')
    update_ratings.short_description = "Update ratings for selected products"


@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    """
    Admin interface for review reports.
    """
    list_display = [
        'review', 'reporter', 'reason', 'status', 'created_at'
    ]
    list_filter = ['reason', 'status', 'created_at']
    search_fields = [
        'review__user__username', 'reporter__username', 
        'review__product__name', 'description'
    ]
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('review', 'reporter', 'reason', 'description')
        }),
        ('Moderation', {
            'fields': ('status', 'admin_notes', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_resolved', 'mark_dismissed']

    def mark_resolved(self, request, queryset):
        """Mark selected reports as resolved"""
        from django.utils import timezone
        updated = queryset.update(status='resolved', resolved_at=timezone.now())
        self.message_user(request, f'{updated} reports marked as resolved.')
    mark_resolved.short_description = "Mark selected reports as resolved"

    def mark_dismissed(self, request, queryset):
        """Mark selected reports as dismissed"""
        updated = queryset.update(status='dismissed')
        self.message_user(request, f'{updated} reports marked as dismissed.')
    mark_dismissed.short_description = "Mark selected reports as dismissed"
