from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Conversation, Message
from .forms import RegistrationForm, LoginForm


messages = [
    {
        'sender': 'Kimi',
        'subject': 'Moi',
        'content': 'Tässä koko viesti'
    }, 
     {
        'sender': 'Mia',
        'subject': 'Hei',
        'content': 'Uusi viesti'
    }
]

# Create your views here.

def indexPageView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid username or password. Please try again.")
    else:
        form = LoginForm()
    return render(request, "index.html", {"form": form})


def registerPageView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


def logoutPageView(request):
    logout(request)
    return redirect("index")


def homePageView(request):
    context = {
        'messages': messages
        } #{"messages": Message.objects.all()}
    return render(request, "home.html", context)
