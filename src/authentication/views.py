from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import auth
from django.db import Error
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def login(request):
    credentials = {}
    credentials["csrf"] = get_token(request)
    user = auth.authenticate(request=request, username=request.data.get("username"),
                             password=request.data.get("password"))
    if(user):
        auth.login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        credentials["token"] = token.key
        return Response(status=status.HTTP_200_OK, data=credentials)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def sign_up(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = username
    credentials = {}
    data = {}
    if(username and password and email):
        try:
            user = User.objects.create_user(username, email, password)
            if(user):
                credentials["csrf"] = get_token(request)
                auth.login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                credentials["token"] = token.key
            return Response(status=status.HTTP_200_OK, data=credentials)
        except Error as e:
            data["message"] = str(e)
    return Response(status=status.HTTP_409_CONFLICT, data=data)
