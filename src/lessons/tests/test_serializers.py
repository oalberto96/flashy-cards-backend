from django.test import TestCase
from lessons.models import Audience
from lessons.serializers import AudienceSerializer


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
