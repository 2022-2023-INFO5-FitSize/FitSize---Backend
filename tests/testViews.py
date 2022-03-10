from uuid import uuid4
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from polls.models import User

class UserViewSetTestCase(TestCase) :
    def setUp(self):
        self.id = uuid4()
        self.login = "Test"
        self.password = "testpassword"
        self.list_url = reverse('user-list')

    def test_post(self):
          """POST to create a User."""
          data = {
              'id': '9f0f8634-748e-4144-ba90-af1bf0fbaf81',
              'login': 'New name',
              'password': 'New password',
          }
          self.assertEqual(User.objects.count(), 0)
          response = self.client.post(self.list_url, data=data)
          self.assertEqual(response.status_code, status.HTTP_201_CREATED)
          self.assertEqual(User.objects.count(), 1)
          user = User.objects.all().first()
          for field_name in data.keys():
                self.assertEqual(getattr(user, field_name), data[field_name])