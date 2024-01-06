from django.urls import path
from . import views

urlpatterns = [
    path("", views.getroutes, name="routes"),
    path("auth/register/", views.registerUser, name="register"),
    path("auth/login/", views.loginUser, name="login"),
    path("auth/logout/", views.logoutUser, name="logout"),
    path("search/", views.searchNotes, name="search-note"),
    path("notes/", views.getNotes, name="notes"),
    path("notes/create", views.createNote, name="create-note"),
    path("notes/<str:pk>", views.getNote, name="get-note"),
    path("notes/<str:pk>/update", views.updateNote, name="update-note"),
    path("notes/<str:pk>/delete", views.deleteNote, name="delete-note"),
    path("notes/<str:pk>/share", views.shareNote, name="share-note"),
]
