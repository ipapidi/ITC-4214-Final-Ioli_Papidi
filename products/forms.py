from django import forms
from .models import ProductRating, Product, Category, Brand
from django.core.exceptions import ValidationError

class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rating']
        widgets = {
            'rating': forms.HiddenInput(),
        }

class VendorProductForm(forms.ModelForm):
    """Form for vendors to create and edit products"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock_quantity', 'main_image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'placeholder': 'Product Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'rows': 4,
                'placeholder': 'Product description...'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select bg-dark text-light border-secondary'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'min': '0',
                'placeholder': '0'
            }),
            'main_image': forms.FileInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active categories
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        
        # Add help text for image upload
        self.fields['main_image'].help_text = "Upload a high-quality image of your F1 part (JPG, PNG, GIF, WebP up to 5MB)"
    
    def clean_main_image(self):
        """Custom validation for main_image"""
        image = self.cleaned_data.get('main_image')
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("File size cannot exceed 5MB")
            
            # Check file type
            import os
            ext = os.path.splitext(image.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            if ext not in valid_extensions:
                raise ValidationError('Only image files (JPG, PNG, GIF, WebP) are allowed.')
        
        return image 