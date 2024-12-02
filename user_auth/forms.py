from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(UserCreationForm):
    ROLE_CHOICES = [
        ('creator', 'Creator'),
        ('taker', 'Taker'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Role")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']

