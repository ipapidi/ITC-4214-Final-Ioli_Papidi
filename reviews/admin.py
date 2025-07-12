from django.contrib import admin
from django.utils.html import format_html
from .models import Review, ProductRating


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for simplified reviews (ratings only).
    """
    list_display = [
        'user', 'product', 'rating_display', 'created_at'
    ]
    list_filter = [
        'rating', 'created_at', 'product__category', 'product__brand'
    ]
    search_fields = [
        'user__username', 'user__email', 'product__name', 'product__sku'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Rating Information', {
            'fields': ('user', 'product', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def rating_display(self, obj):
        """Display rating as stars"""
        return format_html(
            '<span style="color: #ffc107; font-size: 1.2em;">{}</span>',
            obj.rating_stars
        )
    rating_display.short_description = 'Rating'


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    """
    Admin interface for product rating summaries.
    """
    list_display = [
        'product', 'average_rating_display', 'total_reviews',
        'rating_percentage', 'last_updated'
    ]
    list_filter = ['last_updated', 'product__category', 'product__brand']
    search_fields = ['product__name', 'product__sku']
    readonly_fields = [
        'average_rating', 'total_reviews', 'five_star_count', 'four_star_count',
        'three_star_count', 'two_star_count', 'one_star_count', 'last_updated'
    ]
    
    fieldsets = (
        ('Product', {
            'fields': ('product',)
        }),
        ('Rating Statistics', {
            'fields': ('average_rating', 'total_reviews', 'five_star_count', 'four_star_count',
                      'three_star_count', 'two_star_count', 'one_star_count')
        }),
        ('Timestamps', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )

    def average_rating_display(self, obj):
        """Display average rating as stars"""
        return format_html(
            '<span style="color: #ffc107; font-size: 1.2em;">{}</span>',
            obj.rating_stars
        )
    average_rating_display.short_description = 'Average Rating'

    def rating_percentage(self, obj):
        """Display positive rating percentage"""
        return f"{obj.rating_percentage}%"
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
