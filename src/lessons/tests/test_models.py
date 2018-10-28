from django.test import TestCase
from lessons.models import Audience, MediaType


class AudienceModelTest(TestCase):

    def test_model_exist(self):
        audience = Audience()
        self.assertIsInstance(audience, Audience)

    def test_string_representation(self):
        audience = Audience(name="Public")
        self.assertEqual(str(audience), "Public")


class MediaTypeModelTest(TestCase):

    def test_model_exist(self):
        media_type = MediaType()
        self.assertIsInstance(media_type, MediaType)

    def test_string_representation(self):
        media_type = MediaType(name="Image")
        self.assertEqual(str(media_type), "Image")
