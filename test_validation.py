#!/usr/bin/env python3
"""
Comprehensive validation test suite for RevForge
Tests all validation functions to ensure they prevent malicious input
"""

import os
import sys
import django
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.test import Client
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revforge.settings')
django.setup()

from revforge.validators import (
    validate_safe_text, validate_product_name, validate_product_description,
    validate_username, validate_password, validate_phone_number,
    validate_postal_code, validate_address, validate_sku, validate_price,
    validate_stock_quantity, validate_file_name, sanitize_html, validate_email_safe
)
from products.forms import VendorProductForm
from users.forms import UserRegistrationForm


class ValidationTestCase(TestCase):
    """Test case for all validation functions"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_product_name_validation(self):
        """Test product name validation"""
        # Valid names
        valid_names = [
            "F1 Brake Pads",
            "Red Bull Exhaust",
            "Mercedes Suspension",
            "Ferrari Engine Part",
            "McLaren Aerodynamics"
        ]
        
        for name in valid_names:
            try:
                result = validate_product_name(name)
                self.assertEqual(result, name.strip())
            except ValidationError as e:
                self.fail(f"Valid name '{name}' failed validation: {e}")
        
        # Invalid names
        invalid_names = [
            "",  # Empty
            "A",  # Too short
            "A" * 41,  # Too long
            "Product<script>alert('xss')</script>",  # XSS
            "Product with  multiple   spaces",  # Multiple spaces
            "CLICK HERE TO BUY NOW",  # Spam
            "Product with < > \" ' chars",  # Harmful chars
            "Product with http://www.example.com",  # URLs
        ]
        
        for name in invalid_names:
            with self.assertRaises(ValidationError):
                validate_product_name(name)
    
    def test_product_description_validation(self):
        """Test product description validation"""
        # Valid descriptions
        valid_descriptions = [
            "High-quality F1 brake pads for maximum performance.",
            "Authentic Red Bull Racing exhaust system.",
            "Professional grade suspension components."
        ]
        
        for desc in valid_descriptions:
            try:
                result = validate_product_description(desc)
                self.assertEqual(result, desc.strip())
            except ValidationError as e:
                self.fail(f"Valid description failed validation: {e}")
        
        # Invalid descriptions
        invalid_descriptions = [
            "",  # Empty
            "Short",  # Too short
            "A" * 1201,  # Too long
            "Description with <script>alert('xss')</script>",  # XSS
            "Click here to buy now!",  # Spam
            "Visit http://www.example.com",  # URLs
        ]
        
        for desc in invalid_descriptions:
            with self.assertRaises(ValidationError):
                validate_product_description(desc)
    
    def test_username_validation(self):
        """Test username validation"""
        # Valid usernames
        valid_usernames = [
            "john_doe",
            "user123",
            "f1_fan",
            "racing_team"
        ]
        
        for username in valid_usernames:
            try:
                result = validate_username(username)
                self.assertEqual(result, username.strip())
            except ValidationError as e:
                self.fail(f"Valid username '{username}' failed validation: {e}")
        
        # Invalid usernames
        invalid_usernames = [
            "",  # Empty
            "ab",  # Too short
            "A" * 21,  # Too long
            "user@name",  # Invalid chars
            "user-name",  # Invalid chars
            "ADMIN",  # Spam
            "user<script>",  # XSS
        ]
        
        for username in invalid_usernames:
            with self.assertRaises(ValidationError):
                validate_username(username)
    
    def test_password_validation(self):
        """Test password validation"""
        # Valid passwords
        valid_passwords = [
            "SecurePass123!",
            "MyF1RacingPassword",
            "Complex_Password_2024"
        ]
        
        for password in valid_passwords:
            try:
                result = validate_password(password)
                self.assertEqual(result, password)
            except ValidationError as e:
                self.fail(f"Valid password failed validation: {e}")
        
        # Invalid passwords
        invalid_passwords = [
            "",  # Empty
            "123",  # Too short
            "password",  # Common password
            "123456",  # Common password
            "admin",  # Common password
            "A" * 129,  # Too long
        ]
        
        for password in invalid_passwords:
            with self.assertRaises(ValidationError):
                validate_password(password)
    
    def test_phone_number_validation(self):
        """Test phone number validation"""
        # Valid phone numbers
        valid_phones = [
            "1234567890",
            "+1-234-567-8900",
            "(123) 456-7890",
            "123 456 7890"
        ]
        
        for phone in valid_phones:
            try:
                result = validate_phone_number(phone)
                self.assertIsNotNone(result)
            except ValidationError as e:
                self.fail(f"Valid phone number '{phone}' failed validation: {e}")
        
        # Invalid phone numbers
        invalid_phones = [
            "123",  # Too short
            "1234567890123456",  # Too long
            "abc123def",  # Non-numeric
        ]
        
        for phone in invalid_phones:
            with self.assertRaises(ValidationError):
                validate_phone_number(phone)
    
    def test_address_validation(self):
        """Test address validation"""
        # Valid addresses
        valid_addresses = [
            "123 Main Street",
            "456 Racing Avenue, Suite 100",
            "789 F1 Boulevard"
        ]
        
        for address in valid_addresses:
            try:
                result = validate_address(address)
                self.assertEqual(result, address.strip())
            except ValidationError as e:
                self.fail(f"Valid address '{address}' failed validation: {e}")
        
        # Invalid addresses
        invalid_addresses = [
            "",  # Empty
            "123",  # Too short
            "A" * 256,  # Too long
            "Address with <script>alert('xss')</script>",  # XSS
            "Visit http://www.example.com",  # URLs
        ]
        
        for address in invalid_addresses:
            with self.assertRaises(ValidationError):
                validate_address(address)
    
    def test_price_validation(self):
        """Test price validation"""
        # Valid prices
        valid_prices = [
            0.01,
            100.50,
            999999.99
        ]
        
        for price in valid_prices:
            try:
                result = validate_price(price)
                self.assertEqual(result, price)
            except ValidationError as e:
                self.fail(f"Valid price {price} failed validation: {e}")
        
        # Invalid prices
        invalid_prices = [
            0,  # Zero
            -1,  # Negative
            1000000,  # Too high
            None,  # None
        ]
        
        for price in invalid_prices:
            with self.assertRaises(ValidationError):
                validate_price(price)
    
    def test_stock_quantity_validation(self):
        """Test stock quantity validation"""
        # Valid quantities
        valid_quantities = [
            0,
            1,
            100,
            999999
        ]
        
        for quantity in valid_quantities:
            try:
                result = validate_stock_quantity(quantity)
                self.assertEqual(result, quantity)
            except ValidationError as e:
                self.fail(f"Valid quantity {quantity} failed validation: {e}")
        
        # Invalid quantities
        invalid_quantities = [
            -1,  # Negative
            1000000,  # Too high
            None,  # None
        ]
        
        for quantity in invalid_quantities:
            with self.assertRaises(ValidationError):
                validate_stock_quantity(quantity)
    
    def test_sku_validation(self):
        """Test SKU validation"""
        # Valid SKUs
        valid_skus = [
            "F1-BRAKE-001",
            "RB_EXHAUST_2024",
            "MERC_SUSP_123"
        ]
        
        for sku in valid_skus:
            try:
                result = validate_sku(sku)
                self.assertEqual(result, sku.upper())
            except ValidationError as e:
                self.fail(f"Valid SKU '{sku}' failed validation: {e}")
        
        # Invalid SKUs
        invalid_skus = [
            "",  # Empty
            "AB",  # Too short
            "A" * 51,  # Too long
            "SKU@123",  # Invalid chars
            "SKU 123",  # Invalid chars
        ]
        
        for sku in invalid_skus:
            with self.assertRaises(ValidationError):
                validate_sku(sku)
    
    def test_sanitize_html(self):
        """Test HTML sanitization"""
        # Test cases
        test_cases = [
            ("<script>alert('xss')</script>Hello", "Hello"),
            ("<p>Hello</p>", "Hello"),
            ("Hello<script>alert('xss')</script>World", "HelloWorld"),
            ("Normal text", "Normal text"),
            ("Text with javascript:alert('xss')", "Text with alert('xss')"),
        ]
        
        for input_text, expected in test_cases:
            result = sanitize_html(input_text)
            self.assertEqual(result, expected)
    
    def test_form_validation(self):
        """Test form validation"""
        # Test VendorProductForm
        form_data = {
            'name': 'Valid Product Name',
            'description': 'This is a valid product description with enough characters.',
            'price': '100.00',
            'stock_quantity': '10',
            'category': '1'  # Assuming category with ID 1 exists
        }
        
        form = VendorProductForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form should be valid: {form.errors}")
        
        # Test invalid form data
        invalid_form_data = {
            'name': '<script>alert("xss")</script>',
            'description': 'Short',
            'price': '-100',
            'stock_quantity': '-10',
            'category': '1'
        }
        
        form = VendorProductForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())
    
    def test_malicious_input_prevention(self):
        """Test prevention of malicious input"""
        malicious_inputs = [
            # SQL Injection
            "'; DROP TABLE products; --",
            "1' OR '1'='1",
            "UNION SELECT * FROM users",
            
            # XSS
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            
            # Directory traversal
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            
            # Command injection
            "| cat /etc/passwd",
            "; rm -rf /",
            
            # File inclusion
            "<?php include('shell.php'); ?>",
            "<?= system($_GET['cmd']); ?>",
        ]
        
        for malicious_input in malicious_inputs:
            # Test with safe_text validation
            with self.assertRaises(ValidationError):
                validate_safe_text(malicious_input)
            
            # Test with product name validation
            with self.assertRaises(ValidationError):
                validate_product_name(malicious_input)
            
            # Test with username validation
            with self.assertRaises(ValidationError):
                validate_username(malicious_input)
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Test very long inputs
        long_input = "A" * 10000
        with self.assertRaises(ValidationError):
            validate_safe_text(long_input)
        
        # Test null bytes
        null_input = "Hello\x00World"
        result = sanitize_html(null_input)
        self.assertEqual(result, "HelloWorld")
        
        # Test control characters
        control_input = "Hello\x01\x02\x03World"
        result = sanitize_html(control_input)
        self.assertEqual(result, "HelloWorld")
        
        # Test unicode characters
        unicode_input = "F1 Racing 🏎️"
        try:
            result = validate_safe_text(unicode_input)
            self.assertEqual(result, unicode_input.strip())
        except ValidationError:
            # Unicode might be filtered, which is acceptable
            pass


def run_validation_tests():
    """Run all validation tests"""
    print("Running RevForge validation tests...")
    print("=" * 50)
    
    # Create test instance
    test_case = ValidationTestCase()
    test_case.setUp()
    
    # Run all test methods
    test_methods = [method for method in dir(test_case) if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        method = getattr(test_case, method_name)
        try:
            method()
            print(f"✅ {method_name}: PASSED")
            passed += 1
        except Exception as e:
            print(f"❌ {method_name}: FAILED - {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Tests completed: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All validation tests passed! Your site is protected against malicious input.")
    else:
        print("⚠️  Some tests failed. Please review the validation logic.")
    
    return failed == 0


if __name__ == "__main__":
    success = run_validation_tests()
    sys.exit(0 if success else 1) 