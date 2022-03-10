import uuid
from django.test import TestCase
from tests.models import ClothingTypeFactory, UserFactory, UserModelFactory, CompanyFactory, CompanyModelFactory, SizeFactory

class FooTest(TestCase):
    def test_instantiation(self):
        q = UserModelFactory(id = uuid.uuid4())
        a = UserFactory()
        v = UserModelFactory(id = uuid.uuid4(), user = a)
        self.assertEqual(a, v.user)
        self.assertNotEqual(q.id, v.id)

        # Simples instanciation des modèles pour vérifier l'absence d'erreur à la création
        w = CompanyModelFactory()
        x = ClothingTypeFactory()
        y = CompanyFactory()
        z = SizeFactory()