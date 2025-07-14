from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=20,
        label='Username',
        help_text='Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg rounded-3 bg-dark text-light',
            'placeholder': 'Username',
            'style': 'color: #e0e0e0;'
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

    def clean(self):
        cleaned_data = super().clean()
        is_vendor = cleaned_data.get('is_vendor')
        vendor_team = cleaned_data.get('vendor_team')
        
        # If user wants to be a vendor, they must select a team
        if is_vendor and not vendor_team:
            raise forms.ValidationError("Please select an F1 team if you want to register as a vendor.")
        
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