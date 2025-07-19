from django import forms
from .models import ProductRating, Product, Category, SubCategory, Brand
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import re

class ProductRatingForm(forms.ModelForm): #Form for product ratings
    class Meta:
        model = ProductRating #Sets the model to ProductRating
        fields = ['rating'] #Sets the fields to rating
        widgets = {
            'rating': forms.HiddenInput(), #Sets the widget to HiddenInput
        }

class VendorProductForm(forms.ModelForm): #Form for vendors to create and edit products
    """Form for vendors to create and edit products"""
    
    # Add custom fields with validation
    name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-light border-secondary',
            'placeholder': 'Product Name (max 40 characters)',
            'maxlength': '40'
        }),
        help_text="Product name (max 40 characters)"
    )
    
    description = forms.CharField(
        max_length=1200,
        widget=forms.Textarea(attrs={
            'class': 'form-control bg-dark text-light border-secondary',
            'rows': 4,
            'placeholder': 'Product description... (max 1200 characters)',
            'maxlength': '1200'
        }),
        help_text="Product description (max 1200 characters)"
    )
    
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        max_value=999999.99,
        widget=forms.NumberInput(attrs={
            'class': 'form-control bg-dark text-light border-secondary',
            'step': '0.01',
            'min': '0.01',
            'max': '999999.99',
            'placeholder': '0.00'
        }),
        help_text="Price (min $0.01, max $999,999.99)"
    )
    
    stock_quantity = forms.IntegerField(
        min_value=0,
        max_value=999999,
        widget=forms.NumberInput(attrs={
            'class': 'form-control bg-dark text-light border-secondary',
            'min': '0',
            'max': '999999',
            'placeholder': '0'
        }),
        help_text="Stock quantity (0-999,999)"
    )
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'subcategory', 'stock_quantity', 'main_image'] #Sets the fields to name, description, price, category, subcategory, stock_quantity and main_image
        widgets = {
            'name': forms.TextInput(attrs={ #Sets the widget to TextInput
                'class': 'form-control bg-dark text-light border-secondary', #Sets the class to form-control bg-dark text-light border-secondary
                'placeholder': 'Product Name' #Sets the placeholder to Product Name
            }),
            'description': forms.Textarea(attrs={ #Sets the widget to Textarea
                'class': 'form-control bg-dark text-light border-secondary', #Sets the class to form-control bg-dark text-light border-secondary
                'rows': 4, #Sets the rows to 4
                'placeholder': 'Product description...' #Sets the placeholder to Product description...
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary', #Sets the class to form-control bg-dark text-light border-secondary
                'step': '0.01', #Sets the step to 0.01
                'min': '0', #Sets the min to 0
                'placeholder': '0.00' #Sets the placeholder to 0.00
            }),
            'category': forms.Select(attrs={ #Sets the widget to Select
                'class': 'form-select bg-dark text-light border-secondary' #Sets the class to form-select bg-dark text-light border-secondary
            }),
            'subcategory': forms.Select(attrs={ #Sets the widget to Select
                'class': 'form-select bg-dark text-light border-secondary' #Sets the class to form-select bg-dark text-light border-secondary
            }),
            'stock_quantity': forms.NumberInput(attrs={ #Sets the widget to NumberInput
                'class': 'form-control bg-dark text-light border-secondary', #Sets the class to form-control bg-dark text-light border-secondary
                'min': '0', #Sets the min to 0
                'placeholder': '0' #Sets the placeholder to 0
            }),
            'main_image': forms.FileInput(attrs={ #Sets the widget to FileInput
                'class': 'form-control bg-dark text-light border-secondary', #Sets the class to form-control bg-dark text-light border-secondary
                'accept': 'image/*' #Sets the accept to image/*
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #Initializes the form
        # Only show active categories
        self.fields['category'].queryset = Category.objects.filter(is_active=True) #Filters the categories to only show active categories
        
        # Only show active subcategories
        self.fields['subcategory'].queryset = SubCategory.objects.filter(is_active=True) #Filters the subcategories to only show active subcategories
        
        # Add help text for image upload
        self.fields['main_image'].help_text = "Upload a high-quality image of your F1 part (JPG, PNG, GIF, WebP up to 5MB)"
    
    def clean_name(self):
        """Custom validation for product name"""
        name = self.cleaned_data.get('name', '').strip()
        
        if len(name) < 3:
            raise ValidationError('Product name must be at least 3 characters long.')
        
        if len(name) > 40:
            raise ValidationError('Product name cannot exceed 40 characters.')
        
        # Check for potentially harmful characters
        harmful_pattern = r'[<>"\']'
        if re.search(harmful_pattern, name):
            raise ValidationError('Product name cannot contain <, >, ", or \' characters.')
        
        # Check for excessive spaces
        if '  ' in name:
            raise ValidationError('Product name cannot contain multiple consecutive spaces.')
        
        # Check for common spam patterns - only flag obvious spam
        spam_patterns = [
            r'\b(click here|buy now|free|discount|sale|offer|limited time)\b',
            r'\b(www\.|http://|https://)\b',
            # Only flag if entire field is all caps (not just individual words)
            r'^[A-Z\s]{10,}$',  # Entire field in caps with 10+ chars
        ]
        
        for pattern in spam_patterns:
            if re.search(pattern, name, re.IGNORECASE):
                raise ValidationError('Product name contains invalid content.')
        
        return name
    
    def clean_description(self):
        """Custom validation for product description"""
        description = self.cleaned_data.get('description', '').strip()
        
        if len(description) < 10:
            raise ValidationError('Product description must be at least 10 characters long.')
        
        if len(description) > 1200:
            raise ValidationError('Product description cannot exceed 1200 characters.')
        
        # Check for potentially harmful content - more specific
        harmful_patterns = [
            r'<script|javascript:|vbscript:|onload=|onerror=',
            # Only flag obvious spam, not legitimate product descriptions
            r'\b(click here to buy|buy now|free shipping|limited time offer)\b',
            r'\b(www\.|http://|https://)\b',
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                raise ValidationError('Product description contains invalid content.')
        
        return description
    
    def clean_price(self):
        """Custom validation for price"""
        price = self.cleaned_data.get('price')
        
        if price is None:
            raise ValidationError('Price is required.')
        
        if price <= 0:
            raise ValidationError('Price must be greater than 0.')
        
        if price > 999999.99:
            raise ValidationError('Price cannot exceed $999,999.99.')
        
        return price
    
    def clean_stock_quantity(self):
        """Custom validation for stock quantity"""
        stock_quantity = self.cleaned_data.get('stock_quantity')
        
        if stock_quantity is None:
            raise ValidationError('Stock quantity is required.')
        
        if stock_quantity < 0:
            raise ValidationError('Stock quantity cannot be negative.')
        
        if stock_quantity > 999999:
            raise ValidationError('Stock quantity cannot exceed 999,999.')
        
        return stock_quantity
    
    def clean_main_image(self):
        """Custom validation for main_image"""
        image = self.cleaned_data.get('main_image') #Gets the main image
        if image:
            # Check file size
            if image.size > 5 * 1024 * 1024: #Checks if the file size is greater than 5MB
                raise ValidationError("File size cannot exceed 5MB") 
            
            # Check file type
            import os
            ext = os.path.splitext(image.name)[1].lower() #Gets the extension of the image
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'] #Sets the valid extensions to JPG, JPEG, PNG, GIF and WebP
            if ext not in valid_extensions: #Checks if the extension is not in the valid extensions
                raise ValidationError('Only image files (JPG, PNG, GIF, WebP) are allowed.') #Raises an error if the extension is not in the valid extensions
            
            # Check for potentially harmful file names
            harmful_filename_patterns = [
                r'\.\./',  # Directory traversal
                r'<script',  # Script tags
                r'javascript:',  # JavaScript protocol
                r'vbscript:',  # VBScript protocol
            ]
            
            for pattern in harmful_filename_patterns:
                if re.search(pattern, image.name, re.IGNORECASE):
                    raise ValidationError('Invalid file name detected.')
        
        return image
    
    def clean(self):
        """Overall form validation"""
        cleaned_data = super().clean()
        
        # Additional cross-field validation if needed
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        
        if name and description:
            # Check if description is too similar to name
            if name.lower() in description.lower() and len(description) < 50:
                raise ValidationError('Description should be more detailed and different from the product name.')
        
        return cleaned_data 