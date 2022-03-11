import uuid
from django.test import TestCase
from polls import serializers

from tests.models import UserFactory

class UserSerializer(TestCase):
    def test_model_fields(self):
        user = UserFactory
        serializer = serializers.UserSerializer(user)
        for field_name in [
            'id', 'login', 'password'
        ]:
            self.assertEqual(
                serializer.data[field_name],
                getattr(user, field_name)
            )