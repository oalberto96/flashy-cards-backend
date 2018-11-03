from django.test import TestCase
from django.contrib.auth.models import User
from lessons.models import Audience, MediaType, Media, Card, Lesson, Concept
from lessons.serializers import AudienceSerializer, MediaTypeSerializer, MediaSerializer, CardSerializer, LessonSerializer, ConceptSerializer


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
        self.assertEqual(set(data), set(["name", "id"]))

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
            "id": None,
            "name": "Image"})

    def test_source_content(self):
        data = self.serializer.data
        self.assertEqual(data["source"], self.media_attributes["source"])


class CardSerializerTest(TestCase):

    def setUp(self):
        image_type = MediaType(name="Image")
        dog_picture = Media(media_type=image_type,
                            source="http://test.test.png")
        self.card_attributes = {
            "media": dog_picture,
            "text": "Dog",
            "audio": "http://test.test.mp3"
        }
        self.card = Card(**self.card_attributes)
        self.serializer = CardSerializer(instance=self.card)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data), set(["media", "text", "audio"]))

    def test_media_content(self):
        data = self.serializer.data
        self.assertEqual(
            data["media"], {"media_type": {"id": None, "name": "Image"}, "source": "http://test.test.png"})

    def test_text_content(self):
        data = self.serializer.data
        self.assertEqual(data["text"], self.card_attributes["text"])

    def test_audio_content(self):
        data = self.serializer.data
        self.assertEqual(data["audio"], self.card_attributes["audio"])


class LessonSerializerTest(TestCase):

    def setUp(self):
        self.lesson_attributes = {
            "user": User.objects.create(username="test user"),
            "audience": Audience.objects.create(name="Public"),
            "name": "Animals",
            "description": "Animals in German"
        }
        self.lesson = Lesson.objects.create(**self.lesson_attributes)
        self.serializer = LessonSerializer(instance=self.lesson)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data), set(
            ["id", "audience", "name", "description"]))

    def test_audience_content(self):
        data = self.serializer.data
        self.assertEqual(data["audience"], {"name": "Public"})

    def test_name_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.lesson_attributes["name"])

    def test_description_content(self):
        data = self.serializer.data
        self.assertEqual(data["description"],
                         self.lesson_attributes["description"])

    def test_id_content(self):
        data = self.serializer.data
        self.assertEqual(data["id"], 1)


class ConceptSerializerTest(TestCase):

    def setUp(self):
        self.lesson_attributes = {
            "user": User(username="test user"),
            "audience": Audience(name="Public"),
            "name": "Animals",
            "description": "Animals in German"
        }
        self.card_a = Card(text="Dog")
        self.card_b = Card(text="Hund")
        self.concept_attributes = {
            "lesson": Lesson(**self.lesson_attributes),
            "card_a": self.card_a,
            "card_b": self.card_b
        }
        self.concept = Concept(**self.concept_attributes)
        self.serializer = ConceptSerializer(instance=self.concept)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data), set(["card_a", "card_b"]))

    def test_card_a_content(self):
        data = self.serializer.data
        self.assertEqual(data["card_a"], {
                         "text": "Dog", "media": None, "audio": ""})

    def test_card_b_content(self):
        data = self.serializer.data
        self.assertEqual(data["card_b"], {
                         "text": "Hund", "media": None, "audio": ""})
