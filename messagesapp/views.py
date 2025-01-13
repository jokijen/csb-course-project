from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Conversation, Message
from .forms import RegistrationForm, LoginForm, NewConversationForm


def indexPage(request):
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


def registerPage(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


def logoutPage(request):
    logout(request)
    return redirect("index")


#@login_required
def homePage(request):
    user = request.user
    """
    context = {
        "messages": Message.objects.all()
        }
    """
    conversations = Conversation.objects.filter(
        Q(initiator=user) | Q(receiver=user), 
        deleted=False
    ).order_by("-created")

    return render(request, "home.html", {"conversations": conversations})


#@login_required
def newConversationPage(request):
    if request.method == "POST":
        form = NewConversationForm(request.POST)

        if form.is_valid():
            recipient = form.cleaned_data["recipient"]
            message = form.cleaned_data["message"]

            conversation = Conversation.objects.create(initiator=request.user, receiver=recipient)
            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                conversation=conversation,
                content=message
            )
            return redirect("home")
        
        else:
            return render(request, "new_conversation.html", {"form": form}, {"error": "Could not send message. Please try again."})

    else:
        form = NewConversationForm()

    return render(request, "new_conversation.html", {"form": form})


#@login_required
def conversationDetailPage(request, conversation_id):
    if request.method == "POST":
        pass

    else: 
        conversation = get_object_or_404(Conversation, id=conversation_id)
        messages = conversation.conversations.all().order_by("created")

    return render(request, "conversation_detail.html", {"messages": messages})
