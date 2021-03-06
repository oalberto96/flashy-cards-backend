from django.conf import settings
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from lessons.models import Audience, MediaType, Media, Card, Lesson, Concept

import base64
import os
from datetime import datetime


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
    image_file = serializers.CharField(required=False)
    source = serializers.CharField(max_length=2000, allow_blank=True)

    class Meta:
        model = Media
        fields = ["media_type", "source", "image_file"]

    def validate_image_file(self, value):
        if(value != None):
            try:
                base64.b64encode(b'value')
            except:
                raise serializers.ValidationError(
                    "This is not an base64 string")
        return value


class CardSerializer(serializers.ModelSerializer):
    media = MediaSerializer(allow_null=True)
    audio = serializers.CharField(
        max_length=150, allow_blank=True, required=False, allow_null=True)
    text = serializers.CharField(
        max_length=150, allow_blank=True
    )

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
        media_type_image = MediaType.objects.get(name="IMAGE")
        media_type_gif = MediaType.objects.get(name="GIF")
        if(media):
            media_type_data = media["media_type"]
            media_type = MediaType.objects.get(id=media_type_data["id"])
            if(media_type == media_type_image):
                if(instance.media is None):
                    image_name = self.save_image(media["image_file"])
                    instance.media = Media.objects.create(
                        source=image_name, media_type=media_type)
                else:
                    if "image_file" in media:
                        self.delete_image(instance.media.source)
                        new_image = self.save_image(media["image_file"])
                        instance.media.source = new_image
                    else:
                        instance.media.source = media["source"]
                    instance.media.media_type = media_type
                    instance.media.save()
            elif(media_type_gif == media_type):
                if instance.media is None:
                    instance.media = Media.objects.create(
                        source=media["source"], media_type=media_type_gif
                    )
                else:
                    self.delete_image(instance.media.source)
                    instance.media.source = media["source"]
                    instance.media.save()
        instance.text = validated_data.get("text", instance.text)
        instance.audio = validated_data.get("audio", instance.audio)
        instance.save()
        return instance

    def create(self, validated_data):
        if(validated_data["media"]):
            media = validated_data["media"]
            media_type = MediaType.objects.get(id=media["media_type"]["id"])
            media_type_gif = MediaType.objects.get(name="GIF")
            media_type_image = MediaType.objects.get(name="IMAGE")
            if media_type == media_type_image:
                image_name = self.save_image(media["image_file"])
            elif media_type == media_type_gif:
                image_name = media["source"]
            card_media = Media.objects.create(
                media_type=media_type, source=image_name)
            validated_data["media"] = card_media
        return Card.objects.create(**validated_data)

    def save_image(self, image_file):
        now = datetime.now().timestamp()
        image_name = "cardimage" + str(now) + ".png"
        raw_data = image_file.split(",", 1)[1]
        with open(os.path.join(settings.MEDIA_ROOT, image_name), "wb") as fh:
            fh.write(base64.decodebytes(
                raw_data.encode("utf-8")))
        return image_name

    def delete_image(self, image_path):
        file_path = os.path.join(settings.MEDIA_ROOT, image_path)
        return os.remove(file_path) if os.path.isfile(file_path) else False


class ConceptSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(
        model_field=Concept()._meta.get_field('id'), required=False)
    card_a = CardSerializer()
    card_b = CardSerializer()

    class Meta:
        model = Concept
        fields = ["id", "card_a", "card_b"]


class LessonSerializer(serializers.ModelSerializer):
    audience = AudienceSerializer()
    concepts = ConceptSerializer(required=False, many=True)
    deleted_concepts = serializers.ListField(required=False, allow_null=True,
                                             child=serializers.IntegerField()
                                             )

    class Meta:
        model = Lesson
        fields = ["id", "name", "description",
                  "audience", "concepts", "deleted_concepts"]
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
        if(validated_data.get("concepts")):
            for concept in validated_data.get("concepts"):
                card_a_serializer = CardSerializer(data=concept["card_a"])
                card_a_serializer.is_valid()
                card_a = card_a_serializer.save()
                card_b_serializer = CardSerializer(data=concept["card_b"])
                card_b_serializer.is_valid()
                card_b = card_b_serializer.save()
                concept = Concept()
                concept.card_a = card_a
                concept.card_b = card_b
                concept.lesson = lesson
                concept.save()
        return lesson

    def update(self, instance, validated_data):
        audience_data = validated_data.get("audience")
        audience = Audience.objects.get(id=audience_data["id"])
        instance.audience = validated_data.get(audience, instance.audience)
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get(
            "description", instance.description)
        instance.save()
        if(validated_data.get("concepts")):
            for new_concept_data in validated_data.get("concepts"):
                concept_id = new_concept_data["id"]
                if concept_id > 0:
                    concept = Concept.objects.get(id=new_concept_data["id"])
                    card_a_serializer = CardSerializer(
                        concept.card_a, new_concept_data["card_a"])
                    card_b_serializer = CardSerializer(
                        concept.card_b, new_concept_data["card_b"])
                    card_a_serializer.is_valid()
                    card_a_serializer.save()
                    card_b_serializer.is_valid()
                    card_b_serializer.save()
                else:
                    card_a_serializer = CardSerializer(
                        data=new_concept_data["card_a"])
                    card_a_serializer.is_valid()
                    card_a = card_a_serializer.save()
                    card_b_serializer = CardSerializer(
                        data=new_concept_data["card_b"])
                    card_b_serializer.is_valid()
                    card_b = card_b_serializer.save()
                    concept = Concept()
                    concept.card_a = card_a
                    concept.card_b = card_b
                    concept.lesson = Lesson.objects.get(
                        id=validated_data["lesson_id"])
                    concept.save()
        deleted_concepts = validated_data.get("deleted_concepts")
        for concept_to_delete_id in deleted_concepts:
            if concept_to_delete_id > 0:
                Concept.objects.filter(id=concept_to_delete_id).delete()
        return instance
