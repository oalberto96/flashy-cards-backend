from django.test import TestCase
from lessons.models import Audience, MediaType, Card, Lesson


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


class CardModelTest(TestCase):

    def setUp(self):
        self.type_image = MediaType(name="Image")

    def test_model_exist(self):
        card = Card()
        self.assertIsInstance(card, Card)

    def test_string_representation(self):
        card = Card(media_type=self.type_image, text="Dog")
        self.assertEqual(str(card), "Dog")


class LessonModelTest(TestCase):

    def setUp(self):
        self.public_audience = Audience(name="Public")

    def test_model_exist(self):
        lesson = Lesson(
            name="Animals", description="Animals in German", audience=self.public_audience)
        self.assertIsInstance(lesson, Lesson)

    def test_model_representation(self):
        lesson = Lesson(
            name="Animals", description="Animals in German", audience=self.public_audience)
        self.assertEqual(str(lesson), "Animals")
