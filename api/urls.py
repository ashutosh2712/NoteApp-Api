from django.urls import path
from . import views

urlpatterns = [
    path("", views.getroutes, name="routes"),
    path("register/", views.registerUser, name="register"),
]
