from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserLoginViewTests(TestCase):
    def set_up(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.login_url = reverse("users:login")

    def test_login_successful(self):
        self.set_up()
        # Test login with valid credentials
        response = self.client.post(self.login_url, {"username": "testuser", "password": "password123"})
        self.assertRedirects(response, reverse("crowd_app:media_index"))

    def test_login_invalid_credentials(self):
        self.set_up()
        # Test login with invalid credentials
        response = self.client.post(self.login_url, {"username": "testuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_login_with_next_redirect(self):
        self.set_up()
        # Test login with "next" parameter
        next_url = reverse("crowd_app:media_index")
        response = self.client.post(self.login_url, {"username": "testuser", "password": "password123", "next": next_url})
        self.assertRedirects(response, next_url)