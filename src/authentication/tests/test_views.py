from django.test import TestCase, Client
from django.urls import resolve
from django.contrib.auth.models import User
from rest_framework import status
from authentication.views import login, sign_up
import json


class LoginAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test", "test@gmail.com", "test123")
        self.client = Client()
        self.login_url = "/api/authentication/login"

    def test_should_url_resolves_to_login_view(self):
        found = resolve(self.login_url)
        self.assertEqual(found.func, login)

    def test_correct_credentials_and_return_csrf_cookie(self):
        user_data = {"username": "test", "password": "test123"}
        response = self.client.post(self.login_url, user_data,
                                    content_type='application/json')
        self.assertIsNotNone(response.data["csrf"])

    def test_correct_credentials_and_return_djrf_token(self):
        user_data = {"username": "test", "password": "test123"}
        response = self.client.post(self.login_url, user_data,
                                    content_type="application/json")
        self.assertIsNotNone(response.data["token"])

    def test_should_return_ok_if_credentials_are_correct(self):
        user_data = {"username": "test", "password": "test123"}
        response = self.client.post(
            self.login_url, user_data, content_type="application/json")

    def test_return_bad_request_if_doesnt_find_user(self):
        user_data = {"username": "otheruser", "password": "123154"}
        response = self.client.post(
            self.login_url, user_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SignUpAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.sign_up_url = "/api/authentication/signup"

    def test_should_url_resolves_to_signup_view(self):
        found = resolve(self.sign_up_url)
        self.assertEqual(found.func, sign_up)
