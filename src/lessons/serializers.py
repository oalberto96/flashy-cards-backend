from rest_framework.serializers import ModelSerializer
from lessons.models import Audience, MediaType


class AudienceSerializer(ModelSerializer):
    class Meta:
        model = Audience
        fields = ["name"]


class MediaTypeSerializer(ModelSerializer):
    class Meta:
        model = MediaType
        fields = ["name"]
