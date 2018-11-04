from django.test import TestCase, Client
from django.urls import resolve, reverse
from rest_framework import status
from lessons.models import Card
from lessons.views import CardViewSet


class CardUrlTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_resolves_to_get_all(self):
        url = "/api/lessons/cards/"
        response = self.client.get(url)
        self.assertLessEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_url_resolves_to_get_detail(self):
        url = "/api/lessons/cards/1/"
        response = self.client.get(url)
        self.assertLessEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_resolves_to_update(self):
        url = "/api/lessons/cards/1/"
        response = self.client.put(url, data={})
        self.assertLessEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_resolves_to_create(self):
        url = "/api/lessons/cards/"
        response = self.client.post(url, data={})
        self.assertLessEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LessonUrlTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.base_url = "/api/lessons/lessons/"

    def test_url_resolves_to_get_all(self):
        response = self.client.get(self.base_url)
        self.assertLessEqual(response.status_code, status.HTTP_200_OK)

    def test_url_resolves_to_get_detail(self):
        response = self.client.get("{}{}/".format(self.base_url, 1))
        self.assertLessEqual(response.status_code, status.HTTP_200_OK)

    def test_url_resolves_to_update(self):
        response = self.client.put("{}{}/".format(self.base_url, 1), {})
        self.assertLessEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_resolves_to_create(self):
        response = self.client.post(self.base_url, {})
        self.assertLessEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_url_resolves_to_delete(self):
        response = self.client.delete("{}{}/".format(self.base_url, "1"))
        self.assertLessEqual(response.status_code, status.HTTP_200_OK)
