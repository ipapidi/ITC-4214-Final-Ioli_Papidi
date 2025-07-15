from django import forms
from .models import ProductRating, Product, Category, Brand
from django.core.exceptions import ValidationError

class ProductRatingForm(forms.ModelForm): #Form for product ratings
    class Meta:
        model = ProductRating #Sets the model to ProductRating
        fields = ['rating'] #Sets the fields to rating
        widgets = {
            'rating': forms.HiddenInput(), #Sets the widget to HiddenInput
        }

class VendorProductForm(forms.ModelForm): #Form for vendors to create and edit products
    """Form for vendors to create and edit products"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock_quantity', 'main_image'] #Sets the fields to name, description, price, category, stock_quantity and main_image
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
        
        # Add help text for image upload
        self.fields['main_image'].help_text = "Upload a high-quality image of your F1 part (JPG, PNG, GIF, WebP up to 5MB)"
    
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
        
        return image 