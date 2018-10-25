from django.shortcuts import render
from django.middleware.csrf import get_token
from django.contrib import auth
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
