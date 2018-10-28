from django.test import TestCase
from lessons.models import Audience, MediaType
from lessons.serializers import AudienceSerializer, MediaTypeSerializer


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
