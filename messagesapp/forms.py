from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm): # Form for registering new user
    email = forms.EmailField(required=True)
    usable_password = None # Get rid of box asking the user about "Password-based authentication"

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form): # For logging in existing user
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) 


class NewConversationForm(forms.Form): # For starting a new conversation with any other user
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Recipient",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message...'})
    )
    