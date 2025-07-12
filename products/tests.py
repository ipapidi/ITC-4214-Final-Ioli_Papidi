from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Product, Category, SubCategory, Brand
from users.models import UserProfile
import os

# Create your tests here.

class VendorProductFormTest(TestCase):
    def setUp(self):
        # Create a test user with vendor profile
        self.user = User.objects.create_user(
            username='testvendor',
            email='vendor@test.com',
            password='testpass123'
        )
        # Update the automatically created profile
        self.user_profile = self.user.profile
        self.user_profile.is_vendor = True
        self.user_profile.vendor_status = 'approved'
        self.user_profile.vendor_team = 'Ferrari'
        self.user_profile.save()
        
        # Create test category and subcategory
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        self.subcategory = SubCategory.objects.create(
            name='Test Subcategory',
            category=self.category
        )
        
        # Create test brand
        self.brand = Brand.objects.create(
            name='Ferrari',
            is_f1_team=True,
            is_active=True
        )
        
        self.client = Client()
    
    def test_file_size_validation(self):
        """Test that file size validation works correctly"""
        # Login as vendor
        self.client.login(username='testvendor', password='testpass123')
        
        # Create a file larger than 5MB
        large_file = SimpleUploadedFile(
            "large_image.jpg",
            b"x" * (6 * 1024 * 1024),  # 6MB file
            content_type="image/jpeg"
        )
        
        # Try to create a product with large file
        response = self.client.post(reverse('users:vendor_product_create'), {
            'name': 'Test Product',
            'description': 'Test description',
            'price': '99.99',
            'category': self.category.id,
            'stock_quantity': '10',
            'main_image': large_file,
        })
        
        # Should get validation error
        self.assertContains(response, 'File size cannot exceed 5MB')
    
    def test_file_type_validation(self):
        """Test that file type validation works correctly"""
        # Login as vendor
        self.client.login(username='testvendor', password='testpass123')
        
        # Create an invalid file type
        invalid_file = SimpleUploadedFile(
            "test.txt",
            b"this is not an image",
            content_type="text/plain"
        )
        
        # Try to create a product with invalid file type
        response = self.client.post(reverse('users:vendor_product_create'), {
            'name': 'Test Product',
            'description': 'Test description',
            'price': '99.99',
            'category': self.category.id,
            'stock_quantity': '10',
            'main_image': invalid_file,
        })
        
        # Should get validation error
        self.assertContains(response, 'Only image files')
    
    def test_valid_file_upload(self):
        """Test that valid file upload works correctly"""
        # Login as vendor
        self.client.login(username='testvendor', password='testpass123')
        
        # Create a valid file
        valid_file = SimpleUploadedFile(
            "test_image.jpg",
            b"fake image content",
            content_type="image/jpeg"
        )
        
        # Try to create a product with valid file
        response = self.client.post(reverse('users:vendor_product_create'), {
            'name': 'Test Product',
            'description': 'Test description',
            'price': '99.99',
            'category': self.category.id,
            'stock_quantity': '10',
            'main_image': valid_file,
        })
        
        # Should redirect to dashboard (success)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:vendor_dashboard'))
