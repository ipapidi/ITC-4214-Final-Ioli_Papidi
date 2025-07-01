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

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'username':
                field.widget.attrs.update({
                    'class': 'form-control form-control-lg rounded-3 bg-dark text-light',
                    'placeholder': field.label,
                    'style': 'color: #e0e0e0;'
                })
            field.label = field.label
            # Make help_text subtle
            if field.help_text:
                field.help_text = f'<span style="color:#a0a0a0;font-size:0.95em;">{field.help_text}</span>'

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