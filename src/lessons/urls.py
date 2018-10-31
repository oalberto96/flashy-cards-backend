from django.conf.urls import url, include
from authentication import views
from rest_framework import routers
from lessons.views import CardViewSet


router = routers.SimpleRouter()
router.register(r"cards", CardViewSet, "cards")

urlpatterns = [
    url("/", include(router.urls))
]
