import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from polls.models import User
from tests.models import UserFactory

class UserViewSetTestCase(TestCase) :
    def setUp(self):
        self.user = UserFactory(login='testuser',password='testpassword')
        self.user.save()
        self.client.login(login=self.user.login, password=self.user.password)
        self.list_url = reverse('user-list')

    def testPost(self):
          """POST to create a User."""
          data_user = {
              'id': uuid.uuid4(),
              'login': 'New name',
              'password': 'New password',
          }
          self.assertEqual(User.objects.count(), 0)
          response = self.client.post(self.list_url, data=data_user)
          self.assertEqual(response.status_code, status.HTTP_201_CREATED)
          self.assertEqual(User.objects.count(), 1)
          user = User.objects.all().first()
          for field_name in data_user.keys():
                self.assertEqual(getattr(user, field_name), data_user[field_name])