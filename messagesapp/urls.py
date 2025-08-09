from django.urls import path
from .views import (
    indexPage,
    registerPage,
    forgotPasswordPage,
    resetPasswordPage,
    homePage, 
    logoutPage,
    newConversationPage,
    conversationDetailPage,
)


urlpatterns = [
    path("", indexPage, name="index"),
    path("register/", registerPage, name="register"),
    path("forgot-password/", forgotPasswordPage, name="forgot_password"),
    path("reset-link/", resetPasswordPage, name="reset_link"),
    path("home/", homePage, name="home"),
    path("logout/", logoutPage, name="logout"),
    path("new-conversation/", newConversationPage, name="new_conversation"),
    path("conversation/<int:conversation_id>/", conversationDetailPage, name="conversation_detail"),
]
