from django.conf.urls import url, include
from authentication import views
from rest_framework import routers
from lessons.views import CardViewSet, LessonViewSet


router = routers.SimpleRouter()
router.register(r"cards", CardViewSet, "cards")
router.register(r"lessons", LessonViewSet, "lessons")

urlpatterns = [
    url("/", include(router.urls))
]
