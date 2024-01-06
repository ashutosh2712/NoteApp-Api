from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(["GET"])
def getroutes(request):
    return Response("Welcome to NoteApp")


@api_view(["POST"])
def registerUser(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    confirmPassword = request.data.get("confirmPassword")

    if password != confirmPassword:
        return Response(
            {"error": "Passwords does not match!"}, status=status.HTTP_401_UNAUTHORIZED
        )
    try:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

    except IntegrityError:
        return Response(
            {"error": "User already exists!"}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"success": "User successfully registered"}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def loginUser(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return Response(
            {"success": "User logged in successfully"}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Wrong credential!Try again"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
def logoutUser(request):
    if request.method == "POST":
        logout(request)

        return Response(
            {"success": "User loged out successfully!"}, status=status.HTTP_200_OK
        )
