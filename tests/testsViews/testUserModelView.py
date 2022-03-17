from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from polls.models import UserModel, User, ClothingType
from tests.models import UserModelFactory, UserFactory, ClothingTypeFactory
from rest_framework.test import APIClient

#---------------------------------------------USERMODEL VIEW TESTS-----------------------------------------------------#


class UserModelViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('usermodel-list')

    def testGetAll(self):
        """GET to get all UserModels."""
        usermodel1 = UserModelFactory()
        usermodel2 = UserModelFactory()
        usermodel3 = UserModelFactory()

        usermodel1.user.save()
        usermodel1.clothingtype.save()

        usermodel2.user.save()
        usermodel2.clothingtype.save()

        usermodel3.user.save()
        usermodel3.clothingtype.save()

        usermodel1.save()
        usermodel2.save()
        usermodel3.save()

        self.assertEqual(UserModel.objects.count(), 3)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_usermodels = UserModel.objects.all().order_by('id')
        usermodel1_data = all_usermodels[0]
        usermodel2_data = all_usermodels[1]
        usermodel3_data = all_usermodels[2]
        for field_name in ['id', 'name', 'dimensions']:
            self.assertEqual(getattr(usermodel1, field_name),
                             getattr(usermodel1_data, field_name))
            self.assertEqual(getattr(usermodel2, field_name),
                             getattr(usermodel2_data, field_name))
            self.assertEqual(getattr(usermodel3, field_name),
                             getattr(usermodel3_data, field_name))

    def testGetById(self):
        """GET to get UserModel by Id."""
        usermodel = UserModelFactory()
        usermodel.user.save()
        usermodel.clothingtype.save()
        usermodel.save()
        self.assertEqual(UserModel.objects.count(), 1)
        response = self.client.get(self.list_url + str(usermodel.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usermodel_data = UserModel.objects.all().first()
        for field_name in ['id', 'name', 'dimensions']:
            self.assertEqual(getattr(usermodel, field_name),
                             getattr(usermodel_data, field_name))

    def testPost(self):
        """POST to create a UserModel."""
        user = UserFactory()
        clothingtype = ClothingTypeFactory()

        user.save()
        clothingtype.save()

        data_usermodel = {
            'name': 'New name',
            'dimensions': 'New dimensions',
            'user': user.id,
            'clothingtype': clothingtype.id,
        }
        self.assertEqual(UserModel.objects.count(), 0)
        response = self.client.post(self.list_url, data=data_usermodel, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserModel.objects.count(), 1)
        usermodel = UserModel.objects.all().first()
        for field_name in ['name', 'dimensions']:
            self.assertEqual(getattr(usermodel, field_name),
                             data_usermodel[field_name])
        # Tests for ForeignKey fields
        self.assertIsInstance(getattr(usermodel, 'user'), User)
        self.assertEqual(getattr(usermodel, 'user').id, data_usermodel['user'])
        self.assertIsInstance(getattr(usermodel, 'clothingtype'), ClothingType)
        self.assertEqual(getattr(usermodel, 'clothingtype').id,
                         data_usermodel['clothingtype'])

    def testCreateDimensions(self):
        """POST to create a UserModel."""
        user = UserFactory()
        clothingtype = ClothingTypeFactory()

        user.save()
        clothingtype.save()

        

        data_usermodel = {
            'name': 'New name',
            'dimensions': '1.0,0.1,4.0,2.5,4.0KP0.0,0.5,8.0,7.0,6.0,5.5,1.2,7.8,8.8,0.0,9.4,8.0',
            'user': user.id,
            'clothingtype': clothingtype.id,
        }

        self.assertEqual(UserModel.objects.count(), 0)
        response = self.client.post(
            self.list_url + 'savedimensions/', data_usermodel, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserModel.objects.count(), 1)
        usermodel = UserModel.objects.all().first()
        self.assertEqual(getattr(usermodel, 'name'),
                         data_usermodel['name'])
        # Tests for ForeignKey fields
        self.assertIsInstance(getattr(usermodel, 'user'), User)
        self.assertEqual(getattr(usermodel, 'user').id, data_usermodel['user'])
        self.assertIsInstance(getattr(usermodel, 'clothingtype'), ClothingType)
        self.assertEqual(getattr(usermodel, 'clothingtype').id,
                         data_usermodel['clothingtype'])
        self.assertEqual(len(getattr(usermodel, 'dimensions').split(',')), 3)

    def testDelete(self):
        """DELETE to destroy a UserModel."""
        usermodel = UserModelFactory()
        usermodel.user.save()
        usermodel.clothingtype.save()
        usermodel.save()
        self.assertEqual(UserModel.objects.count(), 1)
        response = self.client.delete(
            self.list_url + str(usermodel.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserModel.objects.count(), 0)
