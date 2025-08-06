from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Conversation, Message
from .forms import RegistrationForm, LoginForm, NewConversationForm, NewMessageForm


def indexPage(request):
    if request.user.is_authenticated:
        return redirect("home")

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

    form = LoginForm()
    return render(request, "index.html", {"form": form})


def registerPage(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    form = RegistrationForm()

    return render(request, "register.html", {"form": form})


def logoutPage(request):
    logout(request)
    return redirect("index")


#@login_required
def homePage(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        delete_conversation = request.POST.get("delete")
        if delete_conversation:
            conversation_id = request.POST.get("conversation_id")
            conversation = get_object_or_404(Conversation, id=conversation_id)
            if request.user == conversation.initiator or request.user == conversation.receiver:
                conversation.deleted = True
                conversation.save()
                return redirect("home")

    user_id = request.user.id

    conversations = Conversation.objects.filter(
        Q(initiator_id=user_id) | Q(receiver_id=user_id), 
        deleted=False
    ).order_by("-created")

    return render(request, "home.html", {"conversations": conversations})


#@login_required
def newConversationPage(request):
    if not request.user.is_authenticated:
        return redirect('index')
        
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
        
        return render(request, "new_conversation.html", {"form": form, "error": "Could not send message. Please try again."})

    form = NewConversationForm()

    return render(request, "new_conversation.html", {"form": form})


#@login_required
def conversationDetailPage(request, conversation_id):
    if not request.user.is_authenticated:
        return redirect('index')
    
    # Get the conversation and verify user has access
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user != conversation.initiator and request.user != conversation.receiver:
        return redirect('home')

    if request.method == "POST":
        form = NewMessageForm(request.POST)
        if form.is_valid():
            message_content = form.cleaned_data["message"]

            # Determine the recipient (the other person in the conversation)
            recipient = conversation.receiver if request.user == conversation.initiator else conversation.initiator

            # Create the new message
            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                conversation=conversation,
                content=message_content
            )

            # Redirect to avoid re-submission on page refresh
            return redirect('conversation_detail', conversation_id=conversation_id)

    form = NewMessageForm()

    # Get all messages in the conversation
    messages = conversation.messages.all().order_by("created")

    return render(request, "conversation_detail.html", {
        "messages": messages,
        "conversation": conversation,
        "form": form
    })
