from django.db import models

# Create your models here.


class Audience(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class MediaType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Card(models.Model):
    media_type = models.ForeignKey(
        MediaType, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=150)
    audio = models.CharField(max_length=2000)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
