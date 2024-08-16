from django.urls import path
from .views import (
    indexPageView,
    registerPageView,
    homePageView, 
    logoutPageView # newPageView, loginPageView, messagePageView, replyPageView, deletePageView
)


urlpatterns = [
    path("", indexPageView, name="index"),
    path("register/", registerPageView, name="register"),
    path("home/", homePageView, name="home"),
    path("logout/", logoutPageView, name="logout"),
]

"""
    ,
    path("login/", loginPageView, name="login"),
    path("new-message/", newPageView, name="new_message"),
    path("message/", messagePageView, name="view_message"),
    path("reply/", replyPageView, name="reply"),
    path("delete-message/", deletePageView, name="delete_message"),
"""