from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from polls.models import User
from tests.models import UserFactory
from rest_framework.test import APIClient

#---------------------------------------------USER VIEW TESTS-----------------------------------------------------#


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('user-list')

    def testGetAll(self):
        """GET to get all Users."""
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()
        user1.save()
        user2.save()
        user3.save()
        self.assertEqual(User.objects.count(), 3)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_users = User.objects.all().order_by('id')
        user1_data = all_users[0]
        user2_data = all_users[1]
        user3_data = all_users[2]
        for field_name in ['id', 'login', 'password']:
            self.assertEqual(getattr(user1, field_name),
                             getattr(user1_data, field_name))
            self.assertEqual(getattr(user2, field_name),
                             getattr(user2_data, field_name))
            self.assertEqual(getattr(user3, field_name),
                             getattr(user3_data, field_name))

    def testGetById(self):
        """GET to get User by Id."""
        user = UserFactory()
        user.save()
        self.assertEqual(User.objects.count(), 1)
        response = self.client.get(self.list_url + str(user.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_data = User.objects.all().first()
        for field_name in ['id', 'login', 'password']:
            self.assertEqual(getattr(user, field_name),
                             getattr(user_data, field_name))

    def testPost(self):
        """POST to create a User."""
        data_user = {
            'login': 'New name',
            'password': 'New password',
        }
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(self.list_url, data=data_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.all().first()
        for field_name in data_user.keys():
            self.assertEqual(getattr(user, field_name), data_user[field_name])

    def testDelete(self):
        """DELETE to destroy a User."""
        user = UserFactory()
        user.save()
        self.assertEqual(User.objects.count(), 1)
        response = self.client.delete(self.list_url + str(user.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
