from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework import status
from lessons.models import Card, MediaType, Audience, Lesson, Concept
import json


class CardViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.base_url = "/api/lessons/cards/"
        self.content_type = {
            "content_type": "application/json"
        }

        self.dog_card_attributes = {
            "text": "Dog",
            "media": None,
            "audio": ""
        }
        self.hund_card_attributes = {
            "text": "Hund",
            "media": None,
            "audio": ""
        }
        MediaType.objects.create(name="Image")
        Card.objects.create(**self.dog_card_attributes)
        Card.objects.create(**self.hund_card_attributes)

    def test_get_all_objects(self):
        response = self.client.get(
            self.base_url, **self.content_type)
        data = response.json()
        self.assertEqual(
            data, [{**self.dog_card_attributes}, {**self.hund_card_attributes}])

    def test_retrieve_an_object(self):
        response = self.client.get(
            "{}{}/".format(self.base_url, "1"), **self.content_type)
        data = response.json()
        self.assertEqual(data, self.dog_card_attributes)

    def test_handle_retrieve_a_non_existent_id(self):
        response = self.client.get(
            "{}{}/".format(self.base_url, "5"), **self.content_type)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_handle_retrieve_a_non_integer_id(self):
        response = self.client.get(
            "{}{}/".format(self.base_url, "a"), **self.content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_an_object(self):
        new_dog_attributes = {
            "text": "New Dog",
            "media": None,
            "audio": ""
        }
        self.client.put(
            "{}{}/".format(self.base_url, "1"),
            new_dog_attributes,
            **self.content_type
        )
        new_dog = Card.objects.get(id=1)
        self.assertEqual(new_dog.text, new_dog_attributes["text"])

    def test_update_an_object_with_media_object(self):
        new_dog_attributes = {
            "text": "Dogo",
            "media": {
                "media_type": {
                    "id": 1,
                },
                "source": "http://test.test.png"
            },
            "audio": ""
        }
        self.client.put(
            "{}{}/".format(self.base_url, "1"),
            new_dog_attributes,
            **self.content_type
        )
        dog_updated = Card.objects.get(id=1)
        self.assertEqual(dog_updated.media.source, "http://test.test.png")

    def test_update_an_object_with_a_non_existent_media_type(self):
        new_dog_attributes = {
            "text": "Dogo",
            "media": {
                "media_type": {
                    "id": 5,
                },
                "source": "http://test.test.png"
            },
            "audio": ""
        }
        response = self.client.put(
            "{}{}/".format(self.base_url, "1"),
            new_dog_attributes,
            **self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_an_new_object(self):
        cat_card_attributes = {
            "text": "cat",
            "media": None,
            "audio": ""
        }
        response = self.client.post(
            self.base_url,
            cat_card_attributes,
            **self.content_type)
        cat = Card.objects.get(text="cat")
        self.assertEqual(cat.text, cat_card_attributes["text"])

    def test_create_an_new_object_with_media_content(self):
        kot_card_attributes = {
            "text": "Kot",
            "media": {
                "media_type": {
                    "id": 1,
                },
                "source": "http://test.meaw.png"
            },
            "audio": ""
        }
        self.client.post(
            self.base_url,
            kot_card_attributes,
            **self.content_type)
        card = Card.objects.get(text=kot_card_attributes["text"])
        self.assertEqual(card.media.source,
                         kot_card_attributes["media"]["source"])

    def test_create_an_object_with_invalid_data(self):
        cat_card_attributes = {
            "text": "cat",
            "media": 5,
            "audio": ""
        }
        response = self.client.post(self.base_url, cat_card_attributes,
                                    **self.content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_object(self):
        cards_count = len(Card.objects.all())
        self.client.delete("{}{}/".format(self.base_url, "1"))
        new_cards_count = len(Card.objects.all())
        self.assertLess(new_cards_count, cards_count)

    def test_destroy_a_non_existent_object(self):
        response = self.client.delete("{}{}/".format(self.base_url, "54"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LessonViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="test_user")
        self.client.force_login(self.user)
        self.base_url = "/api/lessons/lessons/"
        self.content_type = {
            "content_type": "application/json"
        }
        self.animals_lesson_attributes = {
            "name": "Animals in german",
            "description": "a little description",
            "audience": Audience.objects.create(name="Public"),
            "user": self.user
        }
        MediaType.objects.create(name="Image")
        Lesson.objects.create(**self.animals_lesson_attributes)

    def test_create_new_lesson(self):
        food_lesson_attributes = {
            "name": "Food",
            "description": "little description",
            "audience": {
                "id": 1
            }}
        response = self.client.post(
            self.base_url,
            food_lesson_attributes,
            **self.content_type)
        found_lesson = Lesson.objects.get(name="Food")
        self.assertEqual(found_lesson.name, food_lesson_attributes["name"])

    def test_create_new_lesson_with_media_in_cards(self):
        food_lesson_attributes = {
            "name": "Food",
            "description": "little description",
            "audience": {
                "id": 1
            },
            "concepts": [
                {
                    "card_a": {
                        "text": "cat",
                        "media": {
                            "media_type": {
                                "id": 1,
                            },
                            "source": "http://test.test.png"
                        },
                        "audio": ""
                    },
                    "card_b": {
                        "text": "kot",
                        "media": None,
                        "audio": ""
                    }
                }
            ]
        }
        response = self.client.post(
            self.base_url,
            food_lesson_attributes,
            **self.content_type)
        concept = Concept.objects.get(id=1)
        self.assertIsNotNone(concept)

    def test_create_new_lesson_with_concept(self):
        food_lesson_attributes = {
            "name": "Food",
            "description": "little description",
            "audience": {
                "id": 1
            },
            "concepts": [
                {
                    "card_a": {
                        "text": "cat",
                        "media": None,
                        "audio": ""
                    },
                    "card_b": {
                        "text": "kot",
                        "media": None,
                        "audio": ""
                    }
                }
            ]
        }
        response = self.client.post(
            self.base_url,
            food_lesson_attributes,
            **self.content_type)
        concept = Concept.objects.get(id=1)
        self.assertIsNotNone(concept)

    def test_create_new_lesson_with_wrong_data(self):
        food_lesson_attributes = {
            "name": "Not food",
            "description": "little description",
        }
        response = self.client.post(
            self.base_url,
            food_lesson_attributes,
            **self.content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_lesson(self):
        new_animals_lesson_attributes = {
            "name": "Animals in french",
            "description": "a big description",
            "audience": {
                "id": 1
            }
        }
        self.client.put("{}{}/".format(self.base_url, "1"),
                        new_animals_lesson_attributes, **self.content_type)
        lesson = Lesson.objects.get(name="Animals in french")
        self.assertEqual(lesson.description,
                         new_animals_lesson_attributes["description"])

    def test_update_lesson_with_media_in_cards(self):
        animal_lesson_attributes = {
            "name": "Food",
            "description": "little description",
            "audience": {
                "id": 1
            },
            "concepts": [
                {
                    "card_a": {
                        "text": "cat",
                        "media": {
                            "media_type": {
                                "id": 1,
                            },
                            "source": "http://test.test.png"
                        },
                        "audio": ""
                    },
                    "card_b": {
                        "text": "kot",
                        "media": None,
                        "audio": ""
                    }
                }
            ]
        }

        new_animal_attributes = {
            "name": "Animals",
            "description": "little description",
            "audience": {
                "id": 1
            },
            "concepts": [
                {
                    "id": 1,
                    "card_a": {
                        "text": "cat",
                        "media": {
                            "media_type": {
                                "id": 1,
                            },
                            "source": "http://new.test.png"
                        },
                        "audio": ""
                    },
                    "card_b": {
                        "text": "Katze",
                        "media": None,
                        "audio": ""
                    }
                }
            ]
        }
        self.client.post(
            self.base_url,
            animal_lesson_attributes,
            **self.content_type)
        response = self.client.put("{}{}/".format(
            self.base_url, "1"),
            new_animal_attributes,
            **self.content_type)
        concept = Concept.objects.get(id=1)
        self.assertEqual(concept.card_a.media.source, "http://new.test.png")

    def test_update_lesson_with_a_new_concept(self):
        animal_lesson_attributes = {
            "name": "Food",
            "description": "little description",
            "audience": {
                "id": 1
            },
            "concepts": [
                {
                    "card_a": {
                        "text": "cat",
                        "media": {
                            "media_type": {
                                "id": 1,
                            },
                            "source": "http://test.test.png"
                        },
                        "audio": ""
                    },
                    "card_b": {
                        "text": "kot",
                        "media": None,
                        "audio": ""
                    }
                }
            ]
        }

        new_animal_attributes = {
            "name": "Animals",
            "description": "little description",
            "audience": {
                "id": 1
            },
            "concepts": [
                {
                    "id": 1,
                    "card_a": {
                        "text": "cat",
                        "media": {
                            "media_type": {
                                "id": 1,
                            },
                            "source": "http://test.test.png"
                        },
                        "audio": ""
                    },
                    "card_b": {
                        "text": "Katze",
                        "media": None,
                        "audio": ""
                    }
                },
                {
                    "id": -1,
                    "card_a": {
                        "text": "hund",
                        "media": {
                            "media_type": {
                                "id": 1,
                            },
                            "source": "http://test.hund.png"
                        },
                        "audio": ""
                    },
                    "card_b": {
                        "text": "Dog",
                        "media": None,
                        "audio": ""
                    }
                }
            ]
        }
        self.client.post(
            self.base_url,
            animal_lesson_attributes,
            **self.content_type)
        response = self.client.put("{}{}/".format(
            self.base_url, "1"),
            new_animal_attributes,
            **self.content_type)
        concept = Concept.objects.get(id=2)
        self.assertEqual(concept.card_b.text, "Dog")

    def test_update_a_non_existent_lesson(self):
        new_animals_lesson_attributes = {
            "name": "Animals in french",
            "description": "a big description",
            "audience": {
                "id": 1
            }
        }
        response = self.client.put("{}{}/".format(self.base_url, "56"),
                                   new_animals_lesson_attributes, **self.content_type)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_lessons(self):
        lesson_count = len(Lesson.objects.all())
        response = self.client.get(self.base_url)
        self.assertEqual(len(response.data), lesson_count)

    def test_delete_lesson(self):
        lesson_count = len(Lesson.objects.all())
        self.client.delete("{}{}/".format(self.base_url, "1"))
        new_lesson_count = len(Lesson.objects.all())
        self.assertEqual(new_lesson_count, lesson_count - 1)

    def test_delete_a_non_existen_lesson(self):
        lesson_count = len(Lesson.objects.all())
        self.client.delete("{}{}/".format(self.base_url, "56"))
        new_lesson_count = len(Lesson.objects.all())
        self.assertEqual(new_lesson_count, lesson_count)

    def test_get_lessons_with_concepts(self):
        animal_lesson_attributes = {
            "name": "Food",
            "description": "little description",
            "audience": {
                "id": 1
            },
            "concepts": [
                {
                    "card_a": {
                        "text": "cat",
                        "media": {
                            "media_type": {
                                "id": 1,
                            },
                            "source": "http://test.test.png"
                        },
                        "audio": ""
                    },
                    "card_b": {
                        "text": "kot",
                        "media": None,
                        "audio": ""
                    }
                }
            ]
        }
        self.client.post(
            self.base_url,
            animal_lesson_attributes,
            **self.content_type)
        response = self.client.get("{}{}/concepts/".format(self.base_url, 2))
        self.assertEqual(response.data["concepts"][0]["card_a"]["text"], "cat")
