from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Review(models.Model):
    """
    Product reviews and ratings system.
    Allows users to rate and review products they've purchased.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    
    # Rating (1-5 stars)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    
    # Review content
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Review status
    is_verified_purchase = models.BooleanField(default=False, help_text="User has purchased this product")
    is_approved = models.BooleanField(default=True, help_text="Review approved by admin")
    is_helpful = models.BooleanField(default=False, help_text="Marked as helpful by other users")
    
    # Additional information
    pros = models.TextField(blank=True, help_text="What you liked about this product")
    cons = models.TextField(blank=True, help_text="What you didn't like about this product")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"

    def save(self, *args, **kwargs):
        # Check if user has purchased this product
        if not self.is_verified_purchase:
            from orders.models import Order
            purchased = Order.objects.filter(
                user=self.user,
                items__product=self.product,
                order_status__in=['delivered', 'shipped']
            ).exists()
            self.is_verified_purchase = purchased
        
        super().save(*args, **kwargs)
        
        # Update product's average rating
        self.product.save()

    @property
    def rating_stars(self):
        """Return rating as stars (★★★★☆)"""
        filled_stars = '★' * self.rating
        empty_stars = '☆' * (5 - self.rating)
        return filled_stars + empty_stars

    @property
    def helpful_count(self):
        """Get number of helpful votes"""
        return self.helpful_votes.count()

    @property
    def unhelpful_count(self):
        """Get number of unhelpful votes"""
        return self.unhelpful_votes.count()


class ReviewImage(models.Model):
    """
    Images attached to reviews.
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_images')
    image = models.ImageField(upload_to='reviews/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for review by {self.review.user.username}"


class ReviewVote(models.Model):
    """
    Helpful/unhelpful votes on reviews.
    """
    VOTE_CHOICES = [
        ('helpful', 'Helpful'),
        ('unhelpful', 'Unhelpful'),
    ]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['review', 'user']

    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} on {self.review}"


class ProductRating(models.Model):
    """
    Aggregated product ratings for quick access.
    """
    product = models.OneToOneField('products.Product', on_delete=models.CASCADE, related_name='rating_summary')
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    five_star_count = models.PositiveIntegerField(default=0)
    four_star_count = models.PositiveIntegerField(default=0)
    three_star_count = models.PositiveIntegerField(default=0)
    two_star_count = models.PositiveIntegerField(default=0)
    one_star_count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating summary for {self.product.name}"

    def update_ratings(self):
        """Update aggregated ratings from reviews"""
        reviews = self.product.reviews.filter(is_approved=True)
        
        if reviews.exists():
            # Calculate average rating
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            self.average_rating = round(avg_rating, 2)
            
            # Count reviews by rating
            self.total_reviews = reviews.count()
            self.five_star_count = reviews.filter(rating=5).count()
            self.four_star_count = reviews.filter(rating=4).count()
            self.three_star_count = reviews.filter(rating=3).count()
            self.two_star_count = reviews.filter(rating=2).count()
            self.one_star_count = reviews.filter(rating=1).count()
        else:
            self.average_rating = 0
            self.total_reviews = 0
            self.five_star_count = 0
            self.four_star_count = 0
            self.three_star_count = 0
            self.two_star_count = 0
            self.one_star_count = 0
        
        self.save()

    @property
    def rating_percentage(self):
        """Get percentage of positive reviews (4+ stars)"""
        if self.total_reviews > 0:
            positive_reviews = self.four_star_count + self.five_star_count
            return round((positive_reviews / self.total_reviews) * 100, 1)
        return 0

    @property
    def rating_stars(self):
        """Return average rating as stars (★★★★☆)"""
        avg = int(self.average_rating)
        filled_stars = '★' * avg
        empty_stars = '☆' * (5 - avg)
        return filled_stars + empty_stars


class ReviewReport(models.Model):
    """
    Report inappropriate reviews.
    """
    REPORT_REASONS = [
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('fake', 'Fake Review'),
        ('offensive', 'Offensive Language'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ['review', 'reporter']

    def __str__(self):
        return f"Report on review by {self.review.user.username}"


# Signal to update product ratings when review is saved
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, created, **kwargs):
    """Update product rating when review is saved"""
    product = instance.product
    rating_summary, created = ProductRating.objects.get_or_create(product=product)
    rating_summary.update_ratings()


@receiver(post_delete, sender=Review)
def update_product_rating_on_delete(sender, instance, **kwargs):
    """Update product rating when review is deleted"""
    product = instance.product
    try:
        rating_summary = ProductRating.objects.get(product=product)
        rating_summary.update_ratings()
    except ProductRating.DoesNotExist:
        pass
