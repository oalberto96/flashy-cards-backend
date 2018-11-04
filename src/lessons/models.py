from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Audience(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class MediaType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Media(models.Model):
    media_type = models.ForeignKey(
        MediaType, on_delete=models.SET_NULL, null=True)
    source = models.CharField(max_length=2000)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}: {}".format(self.media_type.name, self.source)


class Card(models.Model):
    media = models.ForeignKey(
        Media, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=150)
    audio = models.CharField(max_length=2000)
    creation_date = models.DateTimeField(auto_now_add=True)
    concepts = []

    def __str__(self):
        return self.text


class Lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audience = models.ForeignKey(
        Audience, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Concept(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    card_a = models.ForeignKey(
        Card, related_name="card_a", on_delete=models.SET_NULL, null=True)
    card_b = models.ForeignKey(
        Card, related_name="card_b", on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.card_a, self.card_b)
