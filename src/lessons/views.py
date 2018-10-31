from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class CardViewSet(ViewSet):

    def list(self, request):
        queryset = []
        return Response(queryset, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_200_OK)

    def create(self, request):
        return Response(status=status.HTTP_200_OK)
