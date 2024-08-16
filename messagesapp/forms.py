from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm): # Form for registering new user
    email = forms.EmailField(required=True)
    usable_password = None # Get rid of box asking the user about "Password-based authentication"

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form): # Form for logging in existing user
    username = forms.CharField()
    password = forms. CharField(widget=forms.PasswordInput) 
