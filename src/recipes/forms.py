from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

DIFFICULTY_CHOICES = [
    ('', 'All'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Intermediate', 'Intermediate'),
    ('Hard', 'Hard'),
]

COOKING_TIME_CHOICES = [
    ('', 'Any time'),
    ('10', 'Less than 10 minutes'),
    ('30', 'Less than 30 minutes'),
    ('60', 'Less than 60 minutes'),
]

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-input'
        })
    )

class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Choose a username',
            'class': 'form-input'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email (optional)',
            'class': 'form-input'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Choose a password',
            'class': 'form-input'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-input'
        })
    )
    
    def clean_username(self):
        """Check if username already exists"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username
    
    def clean(self):
        """Check if passwords match"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data

class RecipeSearchForm(forms.Form):
    recipe_name = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by recipe name...',
            'class': 'search-input'
        })
    )
    
    ingredient = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by ingredient...',
            'class': 'search-input'
        })
    )
    
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'search-select'
        })
    )
    
    cooking_time = forms.ChoiceField(
        choices=COOKING_TIME_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'search-select'
        })
    )
    
    show_chart = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'chart-checkbox'
        })
    )