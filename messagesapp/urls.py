from django.urls import path
from .views import (
    indexPage,
    registerPage,
    homePage, 
    logoutPage,
    newConversationPage,
    conversationDetailPage,
)


urlpatterns = [
    path("", indexPage, name="index"),
    path("register/", registerPage, name="register"),
    path("home/", homePage, name="home"),
    path("logout/", logoutPage, name="logout"),
    path("new-conversation/", newConversationPage, name="new_conversation"),
    path("conversation/<int:conversation_id>/", conversationDetailPage, name="conversation_detail"),
]
# 