from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from . import views, models

# Create your tests here.
class UserCreationTest(TestCase):
    def setUp(self) -> None:
        self.data = {'username': 'username',
                 'password1': 'test_password',
                 'password2': 'test_password'}
        self.client = Client()
        self.url = reverse("create-user")
        self.response = self.client.post(self.url, self.data)

    def test_view(self):
        view = resolve(reverse("create-user"))
        self.assertEqual(view.func, views.create_user)

    def test_is_user_created(self):
        self.assertTrue(User.objects.all().exists())

    def test_is_profile_created(self):
        self.assertTrue(models.UserProfile.objects.all().exists())

