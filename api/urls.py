from django.urls import path
from . import views

urlpatterns = [
    path("", views.getroutes, name="routes"),
    path("auth/register/", views.registerUser, name="register"),
    path("auth/login/", views.loginUser, name="login"),
    path("auth/logout/", views.logoutUser, name="logout"),
]
