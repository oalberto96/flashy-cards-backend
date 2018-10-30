from rest_framework.serializers import ModelSerializer
from lessons.models import Audience, MediaType, Media, Card, Lesson


class AudienceSerializer(ModelSerializer):
    class Meta:
        model = Audience
        fields = ["name"]


class MediaTypeSerializer(ModelSerializer):
    class Meta:
        model = MediaType
        fields = ["name"]


class MediaSerializer(ModelSerializer):
    media_type = MediaTypeSerializer()

    class Meta:
        model = Media
        fields = ["media_type", "source"]


class CardSerializer(ModelSerializer):
    media = MediaSerializer()

    class Meta:
        model = Card
        fields = ["text", "media", "audio"]


class LessonSerializer(ModelSerializer):
    audience = AudienceSerializer()

    class Meta:
        model = Lesson
        fields = ["name", "description", "audience"]
