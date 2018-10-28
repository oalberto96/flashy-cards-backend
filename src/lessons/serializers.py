from rest_framework.serializers import ModelSerializer
from lessons.models import Audience


class AudienceSerializer(ModelSerializer):
    class Meta:
        model = Audience
        fields = ["name"]
