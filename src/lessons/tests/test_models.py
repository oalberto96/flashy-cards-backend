from django.test import TestCase
from lessons.models import Audiences


class AudiencesModelTest(TestCase):

    def test_model_exist(self):
        audience = Audiences()
        self.assertIsInstance(audience, Audiences)

    def test_string_representation(self):
        audience = Audiences(name="Public")
        self.assertEqual(str(audience), "Public")
