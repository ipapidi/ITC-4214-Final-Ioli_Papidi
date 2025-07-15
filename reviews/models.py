from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Review(models.Model):
    # Product reviews - simplified to rating only
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews') #Set the user
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews') #Set the product
    
    # Rating (1-5 stars)
    rating = models.PositiveIntegerField( #Set the rating
        validators=[MinValueValidator(1), MaxValueValidator(5)], #Set the validators
        help_text="Rating from 1 to 5 stars" #Set the help text
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True) #Set the created at
    updated_at = models.DateTimeField(auto_now=True) #Set the updated at

    class Meta:
        unique_together = ['user', 'product'] #Set the unique together
        ordering = ['-created_at'] #Set the ordering

    def __str__(self):
        return f"Rating by {self.user.username} for {self.product.name}" #Set the string representation

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #Save the review
        # Update product's average rating
        self.product.save() #Save the product

    @property
    def rating_stars(self):
        # Return rating as stars
        filled_stars = '★' * self.rating #Set the filled stars
        empty_stars = '☆' * (5 - self.rating) #Set the empty stars
        return filled_stars + empty_stars #Return the filled and empty stars


class ProductRating(models.Model):
    # Product rating summary
    product = models.OneToOneField('products.Product', on_delete=models.CASCADE, related_name='rating_summary') #Set the product
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0) #Set the average rating
    total_reviews = models.PositiveIntegerField(default=0) #Set the total reviews
    five_star_count = models.PositiveIntegerField(default=0) #Set the five star count
    four_star_count = models.PositiveIntegerField(default=0) #Set the four star count
    three_star_count = models.PositiveIntegerField(default=0) #Set the three star count
    two_star_count = models.PositiveIntegerField(default=0) #Set the two star count
    one_star_count = models.PositiveIntegerField(default=0) #Set the one star count
    last_updated = models.DateTimeField(auto_now=True) #Set the last updated

    def __str__(self):
        return f"Rating summary for {self.product.name}" #Set the string representation

    def update_ratings(self):
        # Update aggregated ratings from reviews
        reviews = self.product.reviews.all()
        
        if reviews.exists():
            # Calculate average rating
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] #Get the average rating
            self.average_rating = round(avg_rating, 2) #Set the average rating
            
            # Count reviews by rating
            self.total_reviews = reviews.count() #Set the total reviews
            self.five_star_count = reviews.filter(rating=5).count() #Set the five star count
            self.four_star_count = reviews.filter(rating=4).count() #Set the four star count
            self.three_star_count = reviews.filter(rating=3).count()
            self.two_star_count = reviews.filter(rating=2).count()
            self.one_star_count = reviews.filter(rating=1).count()
        else:
            self.average_rating = 0 #Set the average rating
            self.total_reviews = 0 #Set the total reviews
            self.five_star_count = 0 #Set the five star count
            self.four_star_count = 0
            self.three_star_count = 0
            self.two_star_count = 0
            self.one_star_count = 0
        
        self.save() #Save the product rating

    @property
    def rating_percentage(self):
        # Get percentage of positive reviews
        if self.total_reviews > 0:
            positive_reviews = self.four_star_count + self.five_star_count #Set the positive reviews
            return round((positive_reviews / self.total_reviews) * 100, 1) #Set the positive reviews percentage
        return 0 #Set the positive reviews percentage

    @property
    def rating_stars(self):
        # Return average rating as stars
        avg = int(self.average_rating) #Set the average rating
        filled_stars = '★' * avg #Set the filled stars
        empty_stars = '☆' * (5 - avg) #Set the empty stars
        return filled_stars + empty_stars #Return the filled and empty stars


# Signal to update product ratings when review is saved
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, created, **kwargs):
    # Update product rating when review is saved
    product = instance.product #Get the product
    rating_summary, created = ProductRating.objects.get_or_create(product=product) #Get or create the product rating
    rating_summary.update_ratings() #Update the product rating

@receiver(post_delete, sender=Review) #Signal to update product ratings when review is deleted
def update_product_rating_on_delete(sender, instance, **kwargs): 
    # Update product rating when review is deleted
    product = instance.product
    try:
        rating_summary = ProductRating.objects.get(product=product) #Get the product rating
        rating_summary.update_ratings() #Update the product rating
    except ProductRating.DoesNotExist:
        pass #Do nothing
