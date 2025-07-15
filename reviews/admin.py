from django.contrib import admin
from django.utils.html import format_html
from .models import Review, ProductRating


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for simplified reviews (ratings only).
    """
    list_display = [ #Display the fields in the admin interface
        'user', 'product', 'rating_display', 'created_at'
    ]
    list_filter = [ #Filter the fields in the admin interface
        'rating', 'created_at', 'product__category', 'product__brand'
    ]
    search_fields = [ #Search the fields in the admin interface
        'user__username', 'user__email', 'product__name', 'product__sku'
    ]
    readonly_fields = ['created_at', 'updated_at'] #Exclude the fields from the admin interface
    
    fieldsets = ( #Organize the fields in the admin interface
        ('Rating Information', { #Organize the fields in the admin interface
            'fields': ('user', 'product', 'rating') #Include the fields in the admin interface
        }),
        ('Timestamps', { #Organize the fields in the admin interface
            'fields': ('created_at', 'updated_at'), #Include the fields in the admin interface
            'classes': ('collapse',) #Include the classes in the admin interface
        }),
    )

    def rating_display(self, obj):
        """Display rating as stars"""
        return format_html( #Display the rating as stars
            '<span style="color: #ffc107; font-size: 1.2em;">{}</span>', #Display the rating as stars
            obj.rating_stars #Display the rating as stars
        )
    rating_display.short_description = 'Rating'


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    """
    Admin interface for product rating summaries.
    """
    list_display = [ #Display the fields in the admin interface
        'product', 'average_rating_display', 'total_reviews',
        'rating_percentage', 'last_updated'
    ]
    list_filter = ['last_updated', 'product__category', 'product__brand'] #Filter the fields in the admin interface
    search_fields = ['product__name', 'product__sku'] #Search the fields in the admin interface
    readonly_fields = [ #Exclude the fields from the admin interface
        'average_rating', 'total_reviews', 'five_star_count', 'four_star_count',
        'three_star_count', 'two_star_count', 'one_star_count', 'last_updated'
    ]
    
    fieldsets = ( #Organize the fields in the admin interface
        ('Product', { #Organize the fields in the admin interface
            'fields': ('product',) #Include the fields in the admin interface
        }),
        ('Rating Statistics', { #Organize the fields in the admin interface
            'fields': ('average_rating', 'total_reviews', 'five_star_count', 'four_star_count',
                      'three_star_count', 'two_star_count', 'one_star_count') #Include the fields in the admin interface
        }),
        ('Timestamps', { #Organize the fields in the admin interface
            'fields': ('last_updated',), #Include the fields in the admin interface
            'classes': ('collapse',) #Include the classes in the admin interface
        }),
    )

    def average_rating_display(self, obj):
        """Display average rating as stars"""
        return format_html( #Display the average rating as stars
            '<span style="color: #ffc107; font-size: 1.2em;">{}</span>', #Display the average rating as stars
            obj.rating_stars #Display the average rating as stars
        )
    average_rating_display.short_description = 'Average Rating'

    def rating_percentage(self, obj):
        """Display positive rating percentage"""
        return f"{obj.rating_percentage}%" #Display the positive rating percentage
    rating_percentage.short_description = 'Positive %' #Display the positive rating percentage

    actions = ['update_ratings'] #Update the ratings

    def update_ratings(self, request, queryset):
        """Update ratings for selected products"""
        updated = 0 #Set the updated to 0
        for rating in queryset: #For each rating in the queryset
            rating.update_ratings() #Update the ratings
            updated += 1 #Increment the updated
        self.message_user(request, f'Ratings updated for {updated} products.') #Display the message
    update_ratings.short_description = "Update ratings for selected products" #Display the message
