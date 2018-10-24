from django.test import TestCase
from django.urls import resolve
from authentication.views import login


class LoginAPITest(TestCase):

    def test_should_url_resolves_to_login_view(self):
        found = resolve("/api/authentication/login")
        self.assertEqual(found.func, login)
