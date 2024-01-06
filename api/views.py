from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer


# Create your views here.
@api_view(["GET"])
def getroutes(request):
    return Response("Welcome to NoteApp")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def registerUser(request):
    if request.method == "POST":
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        confirmPassword = request.data.get("confirmPassword")

        if password != confirmPassword:
            return Response(
                {"error": "Passwords does not match!"},
                status=status.HTTP_401_UNAUTHORIZED,
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
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            return Response(
                {"token": token.key, "success": "User logged in successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Wrong credential!Try again"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@api_view(["POST"])
def logoutUser(request):
    if request.method == "POST":
        logout(request)

        return Response(
            {"success": "User loged out successfully!"}, status=status.HTTP_200_OK
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getNotes(request):
    if request.method == "GET":
        user = request.user
        notes = Note.objects.filter(user=user.id)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getNote(request, pk):
    if request.method == "GET":
        try:
            notes = Note.objects.get(id=pk)
        except Note.DoesNotExist():
            return Response(
                {"error": "Note Dosnt exists!"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = NoteSerializer(notes, many=False)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createNote(request):
    if request.method == "POST":
        data = request.data
        user = request.user
        note = Note.objects.create(body=data["body"], user=user)
        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateNote(request, pk):
    if request.method == "PUT":
        data = request.data
        try:
            notes = Note.objects.get(id=pk)
        except Note.DoesNotExist():
            return Response(
                {"error": "Note Dosnt exists!"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = NoteSerializer(instance=notes, data=data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteNote(request, pk):
    try:
        note = Note.objects.get(id=pk)
    except Note.DoesNotExist():
        return Response(
            {"error": "Note Dosnt exists!"}, status=status.HTTP_404_NOT_FOUND
        )
    note.delete()

    return Response("Note Deleted!")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def shareNote(request, pk):
    try:
        note = Note.objects.get(id=pk)
    except Note.DoesNotExist():
        return Response(
            {"error": "Note Dosnt exists!"}, status=status.HTTP_404_NOT_FOUND
        )
    shared_with_user_id = request.data.get("shared_with_user_id")
    note.shared_with.add(shared_with_user_id)

    serializer = NoteSerializer(note)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def searchNotes(request):
    user = request.user
    search_query = request.query_params.get("q", "")
    notes = Note.objects.filter(user=user, body__icontains=search_query)

    serializer = NoteSerializer(notes, many=True)

    return Response(serializer.data)
