from django.test import TestCase, Client
from django.urls import resolve
from django.contrib.auth.models import User
from authentication.views import login


class LoginAPITest(TestCase):
    def setUpModule(self):
        self.user = User.objects.create_user(
            "test", "test@gmail.com", "test123")
        self.client = Client()

    def test_should_url_resolves_to_login_view(self):
        found = resolve("/api/authentication/login")
        self.assertEqual(found.func, login)

    def test_correct_credentials_and_return_csrf_cookie(self):
        user_data = {"username": "test", "password": "test123"}
        response = self.client.post("/api/authentication/login", user_data,
                                    content_type="aplication/json")
        self.assertIsNotNone(response.data["csrf"])
