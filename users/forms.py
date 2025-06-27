from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = UserProfile.ROLE_CHOICES

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Rol")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)