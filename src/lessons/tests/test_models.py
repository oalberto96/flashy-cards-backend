from django.test import TestCase
from lessons.models import Audience


class AudienceModelTest(TestCase):

    def test_model_exist(self):
        audience = Audience()
        self.assertIsInstance(audience, Audience)

    def test_string_representation(self):
        audience = Audience(name="Public")
        self.assertEqual(str(audience), "Public")
