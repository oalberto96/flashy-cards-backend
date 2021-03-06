from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
from lessons.models import Card, Lesson, Concept, TrainingScore, TrainingScoreConcept
from lessons.serializers import CardSerializer, LessonSerializer


class CardViewSet(ViewSet):

    def list(self, request):
        queryset = Card.objects.all()
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            card = Card.objects.get(id=pk)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            card = None
        if(card):
            serializer = CardSerializer(card)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            card = Card.objects.get(id=pk)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        serializer = CardSerializer(card, request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = CardSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        result = Card.objects.filter(id=pk)
        if(len(result) > 0):
            result.delete()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class LessonViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Lesson.objects.filter(user=request.user).order_by('-last_access')
        serializer = LessonSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        lesson = Lesson.objects.get(id = pk)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        try:
            lesson = Lesson.objects.get(id=pk)
        except ObjectDoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        serializer = LessonSerializer(lesson, request.data)
        if serializer.is_valid():
            serializer.save(lesson_id=pk)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = LessonSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save(owner=request.user)
            return Response(status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            Lesson.objects.get(id=pk).delete()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def concepts(self, request, pk=None):
        lesson = Lesson.objects.get(id=pk)
        lesson.save()
        lesson.concepts = [
            concept for concept in Concept.objects.filter(lesson=lesson)]
        serializer = LessonSerializer(instance=lesson)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def training(self, request, pk=None):
        concepts_score = request.data.get("concepts")
        lesson = Lesson.objects.get(id=pk)
        training_score = TrainingScore.objects.create(lesson=lesson)
        training_score.save_concepts_score(concepts_score)
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"])
    def score(self, request, pk=None):
        training_scores = TrainingScore.objects.filter(lesson=pk)
        queryset = TrainingScoreConcept.objects\
                .filter(training_score__lesson=pk,)\
                .annotate(date=TruncDay("training_score__creation_date"))\
                .values("date")\
                .annotate(mistakes=Sum('mistakes'))\
                .values("date", "mistakes")   
        return Response(status=status.HTTP_200_OK, data=queryset)


