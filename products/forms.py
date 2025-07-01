from django import forms
from .models import ProductRating

class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.HiddenInput(),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional review...'}),
        } 