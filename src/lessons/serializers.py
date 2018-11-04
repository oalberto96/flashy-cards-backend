from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from lessons.models import Audience, MediaType, Media, Card, Lesson, Concept


class AudienceSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(
        model_field=Audience()._meta.get_field('id'))

    class Meta:
        model = Audience
        fields = ["id", "name"]
        read_only_fields = ["name"]


class MediaTypeSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(
        model_field=MediaType()._meta.get_field('id'))
    # name = serializers.ModelField(MediaType()._meta.get_field('name'))

    class Meta:
        model = MediaType
        fields = ["id", "name"]
        read_only_fields = ["name"]


class MediaSerializer(serializers.ModelSerializer):
    media_type = MediaTypeSerializer()

    class Meta:
        model = Media
        fields = ["media_type", "source"]


class CardSerializer(serializers.ModelSerializer):
    media = MediaSerializer(allow_null=True)
    audio = serializers.CharField(max_length=150, allow_blank=True)

    class Meta:
        model = Card
        fields = ["text", "media", "audio"]

    def validate_media(self, value):
        if(value != None):
            try:
                MediaType.objects.get(id=value["media_type"]["id"])
            except:
                raise serializers.ValidationError("MediaType doesn't exist")
        return value

    def update(self, instance, validated_data):
        media = validated_data.get("media")
        if(media):
            media_type_data = media["media_type"]
            media_type = MediaType.objects.get(id=media_type_data["id"])
            if(instance.media is None):
                instance.media = Media.objects.create(
                    source=media["source"], media_type=media_type)
            else:
                instance.media.media_type = media_type
                instance.media.source = media["source"]
        instance.text = validated_data.get("text", instance.text)
        instance.audio = validated_data.get("audio", instance.audio)
        instance.save()
        return instance

    def create(self, validated_data):
        if(validated_data["media"]):
            media = validated_data["media"]
            media_type = MediaType.objects.get(id=media["media_type"]["id"])
            card_media = Media.objects.create(
                media_type=media_type, source=media["source"])
            validated_data["media"] = card_media
        return Card.objects.create(**validated_data)


class LessonSerializer(serializers.ModelSerializer):
    audience = AudienceSerializer()

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "audience"]
        read_only_fields = ["id"]

    def validate_audience(self, value):
        if Audience.objects.filter(id=value["id"]).exists():
            return value
        else:
            raise serializers.ValidationError(
                "Audience with id={} doesn't exist".format(value))

    def create(self, validated_data):
        lesson = Lesson()
        audience_data = validated_data.get("audience")
        audience = Audience.objects.get(id=audience_data["id"])
        lesson.name = validated_data.get("name")
        lesson.description = validated_data.get("description")
        lesson.audience = audience
        lesson.user = validated_data.get("owner")
        lesson.save()
        return lesson

    def update(self, instance, validated_data):
        audience_data = validated_data.get("audience")
        audience = Audience.objects.get(id=audience_data["id"])
        instance.audience = validated_data.get(audience, instance.audience)
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get(
            "description", instance.description)
        instance.save()
        return instance


class ConceptSerializer(serializers.ModelSerializer):
    card_a = CardSerializer()
    card_b = CardSerializer()

    class Meta:
        model = Concept
        fields = ["card_a", "card_b"]
