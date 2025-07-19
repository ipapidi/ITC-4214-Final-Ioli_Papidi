from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Product, Category, SubCategory, Brand
from users.models import UserProfile
import os

class VendorProductFormTest(TestCase):
    def setUp(self):
        # Create a test user with vendor profile
        self.user = User.objects.create_user( #Creates a test user
            username='testvendor', #Sets the username to testvendor
            email='vendor@test.com', #Sets the email to vendor@test.com
            password='testpass123' #Sets the password to testpass123
        )
        # Update the automatically created profile
        self.user_profile = self.user.profile #Gets the user profile
        self.user_profile.is_vendor = True #Sets the is_vendor to True
        self.user_profile.vendor_status = 'approved' #Sets the vendor status to approved
        self.user_profile.vendor_team = 'Ferrari' #Sets the vendor team to Ferrari
        self.user_profile.save() #Saves the user profile
        
        # Create test category and subcategory
        self.category = Category.objects.create( #Creates a test category
            name='Test Category', #Sets the name to Test Category
            description='Test category description' #Sets the description to Test category description
        )
        self.subcategory = SubCategory.objects.create( #Creates a test subcategory
            name='Test Subcategory', #Sets the name to Test Subcategory
            category=self.category #Sets the category to the test category
        )
        
        # Create test brand
        self.brand = Brand.objects.create( #Creates a test brand
            name='Ferrari', #Sets the name to Ferrari
            is_f1_team=True, #Sets the is_f1_team to True
            is_active=True #Sets the is_active to True
        )
        
        self.client = Client() #Creates a test client
    
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
        response = self.client.post(reverse('users:vendor_product_create'), { #Posts the request to the vendor product create view
            'name': 'Test Product', #Sets the name to Test Product
            'description': 'Test description', #Sets the description to Test description
            'price': '99.99', #Sets the price to 99.99
            'category': self.category.id, #Sets the category to the test category
            'stock_quantity': '10', #Sets the stock quantity to 10
            'main_image': large_file, #Sets the main image to the large file
        })
        
        # Should get validation error
        self.assertContains(response, 'File size cannot exceed 5MB')
    
    def test_file_type_validation(self):
        """Test that file type validation works correctly"""
        # Login as vendor
        self.client.login(username='testvendor', password='testpass123') #Logs in the test vendor
        
        # Create an invalid file type
        invalid_file = SimpleUploadedFile( #Creates a test file
            "test.txt", #Sets the name to test.txt
            b"this is not an image", #Sets the content to this is not an image
            content_type="text/plain" #Sets the content type to text/plain
        )
        
        # Try to create a product with invalid file type
        response = self.client.post(reverse('users:vendor_product_create'), { #Posts the request to the vendor product create view
            'name': 'Test Product', #Sets the name to Test Product
            'description': 'Test description', #Sets the description to Test description
            'price': '99.99', #Sets the price to 99.99
            'category': self.category.id, #Sets the category to the test category
            'stock_quantity': '10', #Sets the stock quantity to 10
            'main_image': invalid_file, #Sets the main image to the invalid file
        })
        
        # Should get validation error
        self.assertContains(response, 'Only image files') #Checks if the response contains the text Only image files
    
    def test_valid_file_upload(self):
        """Test that valid file upload works correctly"""
        # Login as vendor
        self.client.login(username='testvendor', password='testpass123')
        
        # Create a valid file
        valid_file = SimpleUploadedFile(
            "test_image.jpg", #Sets the name to test_image.jpg
            b"fake image content", #Sets the content to fake image content
            content_type="image/jpeg" #Sets the content type to image/jpeg
        )
        
        # Try to create a product with valid file
        response = self.client.post(reverse('users:vendor_product_create'), { #Posts the request to the vendor product create view
            'name': 'Test Product', #Sets the name to Test Product
            'description': 'Test description', #Sets the description to Test description
            'price': '99.99', #Sets the price to 99.99
            'category': self.category.id, #Sets the category to the test category
            'stock_quantity': '10', #Sets the stock quantity to 10
            'main_image': valid_file, #Sets the main image to the valid file
        })
        
        # Should redirect to dashboard (success)
        self.assertEqual(response.status_code, 302) #Checks if the response status code is 302
        self.assertRedirects(response, reverse('users:vendor_dashboard')) #Checks if the response redirects to the vendor dashboard
