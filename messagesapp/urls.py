from django.urls import path
from .views import (
    indexPage,
    registerPage,
    homePage, 
    logoutPage,
    newConversationPage,
    conversationDetailPage # , loginPageView, messagePageView, replyPageView, deletePageView
)


urlpatterns = [
    path("", indexPage, name="index"),
    path("register/", registerPage, name="register"),
    path("home/", homePage, name="home"),
    path("logout/", logoutPage, name="logout"),
    path("new-conversation/", newConversationPage, name="new_conversation"),
    path("conversation/<int:conversation_id>/", conversationDetailPage, name="conversation_detail"),
]

"""
    ,
    path("login/", loginPageView, name="login"),
    path("message/", messagePageView, name="view_message"),
    path("reply/", replyPageView, name="reply"),
    path("delete-message/", deletePageView, name="delete_message"),
"""