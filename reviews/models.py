from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Review(models.Model):
    # Product reviews - simplified to rating only
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    
    # Rating (1-5 stars)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"Rating by {self.user.username} for {self.product.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update product's average rating
        self.product.save()

    @property
    def rating_stars(self):
        # Return rating as stars
        filled_stars = '★' * self.rating
        empty_stars = '☆' * (5 - self.rating)
        return filled_stars + empty_stars


class ProductRating(models.Model):
    # Product rating summary
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
        # Update aggregated ratings from reviews
        reviews = self.product.reviews.all()
        
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
        # Get percentage of positive reviews
        if self.total_reviews > 0:
            positive_reviews = self.four_star_count + self.five_star_count
            return round((positive_reviews / self.total_reviews) * 100, 1)
        return 0

    @property
    def rating_stars(self):
        # Return average rating as stars
        avg = int(self.average_rating)
        filled_stars = '★' * avg
        empty_stars = '☆' * (5 - avg)
        return filled_stars + empty_stars


# Signal to update product ratings when review is saved
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, created, **kwargs):
    # Update product rating when review is saved
    product = instance.product
    rating_summary, created = ProductRating.objects.get_or_create(product=product)
    rating_summary.update_ratings()

@receiver(post_delete, sender=Review)
def update_product_rating_on_delete(sender, instance, **kwargs):
    # Update product rating when review is deleted
    product = instance.product
    try:
        rating_summary = ProductRating.objects.get(product=product)
        rating_summary.update_ratings()
    except ProductRating.DoesNotExist:
        pass
