from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Insecure way:
SECRET_QUESTION_CHOICES = [
    ('', 'Select a question...'),
    ('pet', 'What is the name of your first pet?'),
    ('school', 'What elementary school did you go to?'),
    ('name', 'What is your mother\'s maiden name?'),
]

class RegistrationForm(UserCreationForm): # Form for registering new user
    email = forms.EmailField(required=True)
    secret_question = forms.ChoiceField(
        choices=SECRET_QUESTION_CHOICES,
        required=True,
        label="Secret Question"
    )
    secret_answer = forms.CharField(required=True, label="Secret Answer")
    usable_password = None # Get rid of box asking the user about "Password-based authentication"

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'secret_question', 'secret_answer']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Store secret answer in the first_name field, as it is a built-in field and easy to use
        user.first_name = self.cleaned_data['secret_answer']
        
        if commit:
            user.save()
        return user

"""
# Secure way:
class RegistrationForm(UserCreationForm): # Form for registering new user
    email = forms.EmailField(required=True)

    usable_password = None # Get rid of box asking the user about "Password-based authentication"

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
"""

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
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message...'
            })
    )


class NewMessageForm(forms.Form): # For adding messages to existing conversations
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Type your message here...'
        })
    )

# Insecure way:
class ForgotPasswordForm(forms.Form): # For resetting password
    email = forms.EmailField(required=True, label="Email Address")
    secret_question = forms.ChoiceField(
        choices=SECRET_QUESTION_CHOICES,
        required=True,
        label="Secret Question"
    )
    secret_answer = forms.CharField(required=True, label="Secret Answer")

#Secure way:
class ResetPasswordForm(forms.Form): # For resetting password
    email = forms.EmailField(required=True, label="Email Address")
