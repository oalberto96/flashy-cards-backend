from django.contrib import admin
from lessons.models import Lesson, Audience, MediaType, Card, TrainingScoreConcept
# Register your models here.

admin.site.register(Lesson)
admin.site.register(Audience)
admin.site.register(MediaType)
admin.site.register(Card)
admin.site.register(TrainingScoreConcept)
