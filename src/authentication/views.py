from django.shortcuts import render
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def login(request):
    credentials = {}
    credentials["csrf"] = get_token(request)
    return Response(status=status.HTTP_200_OK, data=credentials)
