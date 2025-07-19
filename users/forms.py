from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
import re

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=20,
        min_length=3,
        label='Username',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Username can only contain letters, numbers, and underscores.'
            ),
            MinLengthValidator(3, 'Username must be at least 3 characters long.')
        ],
        help_text='Required. 3-20 characters. Letters, digits and underscores only.',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg rounded-3 bg-dark text-light',
            'placeholder': 'Username (3-20 characters)',
            'style': 'color: #e0e0e0;',
            'maxlength': '20',
            'minlength': '3'
        })
    )

    # Vendor registration fields
    is_vendor = forms.BooleanField(
        required=False,
        label='I want to register as a vendor',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'is_vendor_checkbox'
        })
    )
    
    vendor_team = forms.ChoiceField(
        required=False,
        label='F1 Team',
        choices=[
            ('', 'Select an F1 team'),
            ('Ferrari', 'Ferrari'),
            ('Red Bull Racing', 'Red Bull Racing'),
            ('Mercedes', 'Mercedes'),
            ('McLaren', 'McLaren'),
            ('Aston Martin', 'Aston Martin'),
            ('Alpine', 'Alpine'),
            ('Williams', 'Williams'),
            ('AlphaTauri', 'AlphaTauri'),
            ('Alfa Romeo', 'Alfa Romeo'),
            ('Haas', 'Haas'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg rounded-3 bg-dark text-light',
            'id': 'vendor_team_select',
            'style': 'color: #e0e0e0; display: none;'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['username', 'is_vendor', 'vendor_team']:
                field.widget.attrs.update({
                    'class': 'form-control form-control-lg rounded-3 bg-dark text-light',
                    'placeholder': field.label,
                    'style': 'color: #e0e0e0;'
                })
            field.label = field.label
            # Make help_text subtle
            if field.help_text:
                field.help_text = f'<span style="color:#a0a0a0;font-size:0.95em;">{field.help_text}</span>'

    def clean_username(self):
        """Custom validation for username"""
        username = self.cleaned_data.get('username', '').strip()
        
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        
        if len(username) > 20:
            raise ValidationError('Username cannot exceed 20 characters.')
        
        # Check for potentially harmful characters
        harmful_pattern = r'[<>"\']'
        if re.search(harmful_pattern, username):
            raise ValidationError('Username cannot contain <, >, ", or \' characters.')
        
        # Check for excessive spaces
        if '  ' in username:
            raise ValidationError('Username cannot contain multiple consecutive spaces.')
        
        # Check for common spam patterns
        spam_patterns = [
            r'\b(admin|root|test|guest|user|demo)\b',
            r'\b(www\.|http://|https://)\b',
            r'\b[A-Z]{5,}\b',  # All caps words
        ]
        
        for pattern in spam_patterns:
            if re.search(pattern, username, re.IGNORECASE):
                raise ValidationError('Username contains invalid content.')
        
        return username
    
    def clean_password1(self):
        """Custom validation for password"""
        password = self.cleaned_data.get('password1')
        
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        
        if len(password) > 128:
            raise ValidationError('Password cannot exceed 128 characters.')
        
        # Check for common weak passwords
        weak_patterns = [
            r'^123456',
            r'^password',
            r'^qwerty',
            r'^abc123',
            r'^admin',
            r'^test',
        ]
        
        for pattern in weak_patterns:
            if re.search(pattern, password, re.IGNORECASE):
                raise ValidationError('Password is too common. Please choose a stronger password.')
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        is_vendor = cleaned_data.get('is_vendor')
        vendor_team = cleaned_data.get('vendor_team')
        
        # If user wants to be a vendor, they must select a team
        if is_vendor and not vendor_team:
            raise ValidationError("Please select an F1 team if you want to register as a vendor.")
        
        return cleaned_data

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-lg rounded-3 bg-dark text-light',
                'placeholder': field.label,
                'style': 'color: #e0e0e0;'
            })
            field.label = field.label
            if field.help_text:
                field.help_text = f'<span style="color:#a0a0a0;font-size:0.95em;">{field.help_text}</span>' 