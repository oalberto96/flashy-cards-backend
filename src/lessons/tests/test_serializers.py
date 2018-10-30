from django.test import TestCase
from lessons.models import Audience, MediaType, Media
from lessons.serializers import AudienceSerializer, MediaTypeSerializer, MediaSerializer


class AudienceSerializerTest(TestCase):

    def setUp(self):
        self.audience_attributes = {
            "id": 1,
            "name": "Public"
        }
        self.audience = Audience(**self.audience_attributes)
        self.serializer = AudienceSerializer(instance=self.audience)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data), set(["name"]))

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.audience_attributes["name"])


class MediaTypeSerializerTest(TestCase):

    def setUp(self):
        self.media_type_attributes = {
            "name": "Image"
        }
        self.media_type = MediaType(**self.media_type_attributes)
        self.serializer = MediaTypeSerializer(instance=self.media_type)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data), set(["name"]))

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.media_type_attributes["name"])


class MediaSerializerTest(TestCase):

    def setUp(self):
        media_type = MediaType(name="Image")
        self.media_attributes = {
            "media_type": media_type,
            "source": "http://test.test.png"
        }
        self.media = Media(**self.media_attributes)
        self.serializer = MediaSerializer(instance=self.media)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data), set(["source", "media_type"]))

    def test_media_type_content(self):
        data = self.serializer.data
        self.assertEqual(data["media_type"], {
                         "name": "Image"})

    def test_source_content(self):
        data = self.serializer.data
        self.assertEqual(data["source"], self.media_attributes["source"])
